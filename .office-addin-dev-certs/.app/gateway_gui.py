"""
Claude Gateway v1.0 — GUI (customtkinter + pystray)
Portable. System tray on close/minimize.
"""
import json, os, socket, subprocess, sys, threading, time, traceback
from pathlib import Path

_PY = Path(sys.executable).parent
_TCL = _PY / "tcl"
if _TCL.exists():
    os.environ.setdefault("TCL_LIBRARY", str(_TCL / "tcl8.6"))
    os.environ.setdefault("TK_LIBRARY", str(_TCL / "tk8.6"))

APP_DIR     = Path(__file__).parent
LOG_DIR     = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = APP_DIR / "gateway-config.json"
ICON_PATH   = APP_DIR / "icon.ico"
ICON_PNG    = APP_DIR / "icon.png"
_ERR_LOG    = LOG_DIR / "gui-error.log"

def _log(msg):
    try:
        with open(_ERR_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except: pass

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
except Exception as e:
    _log(f"import fail: {e}\n{traceback.format_exc()}"); sys.exit(1)

try:
    import pystray
    from PIL import Image as PILImage
    HAS_TRAY = True
except:
    HAS_TRAY = False

# === THEME ===
BG      = "#0A0D14"
SURF    = "#111827"
SURF2   = "#1F2937"
TXT     = "#F8FAFC"
TXT2    = "#94A3B8"
BRD     = "#374151"
BLUE    = "#3B82F6"
BLUE_H  = "#2563EB"
GREEN   = "#22C55E"
GREEN_H = "#16A34A"
RED     = "#EF4444"
YELLOW  = "#F59E0B"
SP = 16
NO_WIN = 0x08000000
PROXY_URL = "https://localhost:8443"


class GatewayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Claude Gateway v1.0")
        self.configure(fg_color=BG)
        self.resizable(True, True)
        if ICON_PATH.exists():
            try: self.iconbitmap(str(ICON_PATH))
            except: pass

        self._cfg = self._load_cfg()
        self._tray_icon = None
        self._build()

        self.update_idletasks()
        self.geometry("500x370")
        self.minsize(460, 340)
        self._center()

        self.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)
        self.after(400, self._refresh)
        # Auto-poll every 5 seconds
        self._auto_poll()

    def _auto_poll(self):
        self._refresh()
        self.after(5000, self._auto_poll)

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{max((self.winfo_screenwidth()-w)//2,0)}+{max((self.winfo_screenheight()-h)//2,0)}")

    def _load_cfg(self):
        try: return json.loads(CONFIG_PATH.read_text("utf-8"))
        except: return {"mode": "free"}

    def _save_cfg(self, cfg):
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), "utf-8")
        self._cfg = cfg

    def _port_ok(self, p=8443):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1); return s.connect_ex(("127.0.0.1", p)) == 0
        except: return False

    def _find_node(self):
        local = APP_DIR / "node" / "node.exe"
        if local.exists(): return str(local)
        import shutil; return shutil.which("node")

    # ── System tray ──
    def _minimize_to_tray(self):
        if HAS_TRAY:
            self.withdraw()
            if not self._tray_icon:
                self._create_tray()
        else:
            self.iconify()

    def _create_tray(self):
        try:
            if ICON_PNG.exists():
                img = PILImage.open(str(ICON_PNG))
            elif ICON_PATH.exists():
                img = PILImage.open(str(ICON_PATH))
            else:
                img = PILImage.new("RGB", (64, 64), (59, 130, 246))
            menu = pystray.Menu(
                pystray.MenuItem("Abrir Claude Gateway", self._show_from_tray, default=True),
                pystray.MenuItem("Sair", self._quit_from_tray),
            )
            self._tray_icon = pystray.Icon("claude_gw", img, "Claude Gateway v1.0", menu)
            threading.Thread(target=self._tray_icon.run, daemon=True).start()
        except Exception as e:
            _log(f"tray err: {e}"); self.deiconify()

    def _show_from_tray(self, icon=None, item=None):
        if self._tray_icon:
            self._tray_icon.stop(); self._tray_icon = None
        self.after(0, self._restore)

    def _restore(self):
        self.deiconify(); self.lift(); self.focus_force()

    def _quit_from_tray(self, icon=None, item=None):
        if self._tray_icon:
            self._tray_icon.stop(); self._tray_icon = None
        self.after(0, self.destroy)

    # ── Actions ──
    def _start(self):
        self._btn_start.configure(state="disabled", text="Iniciando...")
        self.update()
        threading.Thread(target=self._do_start, daemon=True).start()

    def _do_start(self):
        subprocess.run(
            ["powershell", "-WindowStyle", "Hidden", "-Command",
             "netstat -ano 2>$null | Select-String ':8443.*LISTENING' | ForEach-Object "
             "{ $p = ($_.ToString().Trim() -split '\\s+')[-1]; if ($p -match '^\\d+$') "
             "{ Stop-Process -Id ([int]$p) -Force -EA SilentlyContinue } }"],
            capture_output=True, creationflags=NO_WIN)
        time.sleep(1)
        node = self._find_node()
        if not node:
            self.after(0, lambda: self._btn_start.configure(state="normal", text="▶  Iniciar"))
            return
        with open(LOG_DIR / "proxy-error.log", "w") as ef:
            subprocess.Popen([node, str(APP_DIR / "proxy-cors.js")],
                stdout=subprocess.DEVNULL, stderr=ef, cwd=str(APP_DIR), creationflags=NO_WIN)
        time.sleep(2)
        self.after(0, self._refresh)

    def _stop(self):
        self._btn_stop.configure(state="disabled", text="Parando...")
        self.update()
        threading.Thread(target=self._do_stop, daemon=True).start()

    def _do_stop(self):
        subprocess.run(
            ["powershell", "-WindowStyle", "Hidden", "-Command",
             "netstat -ano 2>$null | Select-String ':8443.*LISTENING' | ForEach-Object "
             "{ $p = ($_.ToString().Trim() -split '\\s+')[-1]; if ($p -match '^\\d+$') "
             "{ Stop-Process -Id ([int]$p) -Force -EA SilentlyContinue } }"],
            capture_output=True, creationflags=NO_WIN)
        time.sleep(1)
        self.after(0, self._refresh)

    def _set_mode(self, mode):
        cfg = self._load_cfg()
        cfg["mode"] = mode
        self._save_cfg(cfg)
        self._refresh()

    def _copy_url(self):
        self.clipboard_clear()
        self.clipboard_append(PROXY_URL)
        self._btn_copy.configure(text="Copiado ✓")
        self.after(2000, lambda: self._btn_copy.configure(text="Copiar"))

    def _refresh(self):
        self._cfg = self._load_cfg()
        active = self._port_ok(8443)
        mode = self._cfg.get("mode", "free")

        # Proxy status badge
        if active:
            self._dot.configure(fg_color=GREEN)
            self._lbl_st.configure(text="ATIVO", text_color=GREEN)
        else:
            self._dot.configure(fg_color=RED)
            self._lbl_st.configure(text="INATIVO", text_color=RED)

        # URL visibility
        if active:
            self._url_frame.pack(fill="x", pady=(8, 0), after=self._row_title)
        else:
            self._url_frame.pack_forget()

        # Button states
        self._btn_start.configure(
            state="disabled" if active else "normal",
            text="▶  Iniciar",
            fg_color=BRD if active else BLUE)
        self._btn_stop.configure(
            state="disabled" if not active else "normal",
            text="■  Parar",
            fg_color=BRD if not active else RED)

        # Mode buttons
        if mode == "free":
            self._sw_free.configure(fg_color=GREEN, hover_color=GREEN_H, text_color="white")
            self._sw_paid.configure(fg_color=SURF2, hover_color=BLUE_H, text_color=TXT2)
        else:
            self._sw_free.configure(fg_color=SURF2, hover_color=GREEN_H, text_color=TXT2)
            self._sw_paid.configure(fg_color=BLUE, hover_color=BLUE_H, text_color="white")

    # ── Build ──
    def _build(self):
        fH = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        fS = ctk.CTkFont(family="Segoe UI", size=13)
        fB = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        fX = ctk.CTkFont(family="Segoe UI", size=11)
        fU = ctk.CTkFont(family="Segoe UI", size=12)
        fF = ctk.CTkFont(family="Segoe UI", size=10)

        # ─── Header ───
        hdr = ctk.CTkFrame(self, fg_color=SURF, corner_radius=0)
        hdr.pack(fill="x")
        hi = ctk.CTkFrame(hdr, fg_color="transparent")
        hi.pack(fill="x", padx=SP, pady=10)
        bar = ctk.CTkFrame(hi, fg_color=BLUE, width=4, height=36, corner_radius=2)
        bar.pack(side="left", padx=(0, 12)); bar.pack_propagate(False)
        tt = ctk.CTkFrame(hi, fg_color="transparent")
        tt.pack(side="left")
        ctk.CTkLabel(tt, text="Claude Gateway", font=fH, text_color=TXT).pack(anchor="w")
        ctk.CTkLabel(tt, text="Proxy para Office Add-in", font=fS, text_color=TXT2).pack(anchor="w")

        ctk.CTkFrame(self, fg_color=BRD, height=1, corner_radius=0).pack(fill="x")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=SP, pady=(SP, 6))

        # ─── Card: Proxy ───
        c1 = ctk.CTkFrame(body, fg_color=SURF, corner_radius=8)
        c1.pack(fill="x", pady=(0, 10))
        c1i = ctk.CTkFrame(c1, fg_color="transparent")
        c1i.pack(fill="x", padx=SP, pady=10)

        # Title + badge on same line
        self._row_title = ctk.CTkFrame(c1i, fg_color="transparent")
        self._row_title.pack(fill="x")
        ctk.CTkLabel(self._row_title, text="Proxy", font=fB, text_color=TXT).pack(side="left")
        badge = ctk.CTkFrame(self._row_title, fg_color="transparent")
        badge.pack(side="right")
        self._dot = ctk.CTkFrame(badge, fg_color=RED, width=8, height=8, corner_radius=4)
        self._dot.pack(side="left", padx=(0, 5)); self._dot.pack_propagate(False)
        self._lbl_st = ctk.CTkLabel(badge, text="INATIVO", font=fB, text_color=RED)
        self._lbl_st.pack(side="left")

        # URL (hidden by default, shown only when active)
        self._url_frame = ctk.CTkFrame(c1i, fg_color=SURF2, corner_radius=6)
        # NOT packed yet — will be packed in _refresh when active
        self._lbl_url = ctk.CTkLabel(self._url_frame, text=PROXY_URL, font=fU, text_color=BLUE)
        self._lbl_url.pack(side="left", padx=10, pady=5)
        self._btn_copy = ctk.CTkButton(self._url_frame, text="Copiar", font=fX, width=60, height=24,
            fg_color=BLUE, hover_color=BLUE_H, command=self._copy_url)
        self._btn_copy.pack(side="right", padx=6, pady=4)

        # Buttons (only Start and Stop — no Status)
        btns = ctk.CTkFrame(c1i, fg_color="transparent")
        btns.pack(fill="x", pady=(10, 0))
        btns.grid_columnconfigure((0, 1), weight=1)
        self._btn_start = ctk.CTkButton(btns, text="▶  Iniciar", font=fB, height=34,
            fg_color=BLUE, hover_color=BLUE_H, command=self._start)
        self._btn_start.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self._btn_stop = ctk.CTkButton(btns, text="■  Parar", font=fB, height=34,
            fg_color=BRD, hover_color="#B91C1C", command=self._stop, state="disabled")
        self._btn_stop.grid(row=0, column=1, sticky="ew")

        # ─── Card: Mode ───
        c2 = ctk.CTkFrame(body, fg_color=SURF, corner_radius=8)
        c2.pack(fill="x")
        c2i = ctk.CTkFrame(c2, fg_color="transparent")
        c2i.pack(fill="x", padx=SP, pady=10)
        ctk.CTkLabel(c2i, text="Modo de Operação", font=fB, text_color=TXT).pack(anchor="w")

        # Two separate buttons
        sw = ctk.CTkFrame(c2i, fg_color="transparent")
        sw.pack(fill="x", pady=(8, 0))
        sw.grid_columnconfigure((0, 1), weight=1)
        self._sw_free = ctk.CTkButton(sw, text="Gratuito", font=fB, height=34,
            corner_radius=6, fg_color=GREEN, hover_color=GREEN_H, text_color="white",
            command=lambda: self._set_mode("free"))
        self._sw_free.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self._sw_paid = ctk.CTkButton(sw, text="Pago (Claude)", font=fB, height=34,
            corner_radius=6, fg_color=SURF2, hover_color=BLUE_H, text_color=TXT2,
            command=lambda: self._set_mode("paid"))
        self._sw_paid.grid(row=0, column=1, sticky="ew")

        # ─── Footer ───
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=SP, pady=(0, 8))
        ctk.CTkLabel(footer, text="Desenvolvido por Bruno Ferreira", font=fF, text_color=TXT2).pack(side="left")
        ctk.CTkLabel(footer, text="v1.0", font=fF, text_color=TXT2).pack(side="right")


if __name__ == "__main__":
    try:
        app = GatewayApp()
        app.mainloop()
    except Exception as e:
        _log(f"FATAL: {e}\n{traceback.format_exc()}")
        sys.exit(1)
