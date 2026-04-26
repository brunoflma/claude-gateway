# ⚡ Claude Gateway

Proxy local para o Claude for Office Add-in — permite usar modelos de IA gratuitos (DeepSeek, GLM) ou pagos diretamente no Word, Excel e PowerPoint, via ZenMux.

---

## O problema

O Claude for Office Add-in requer uma chave API paga da Anthropic para funcionar. Não há opção gratuita nativa, e muitos usuários não têm acesso direto à API.

## A solução

O Claude Gateway é um proxy HTTPS local que intercepta as requisições do add-in e as redireciona para o ZenMux — um gateway que oferece acesso gratuito a modelos como DeepSeek e GLM, ou acesso pago a modelos Claude reais.

```
Word/Excel/PowerPoint → Add-in Claude → Proxy local (HTTPS) → ZenMux → Modelo de IA
```

**Características:**
- Proxy HTTPS local com certificado SSL incluso
- Interface gráfica para controle (iniciar/parar/configurar)
- Node.js e Python embutidos — instalação zero dependências
- Suporte a Windows e macOS
- Mapeamento automático de modelos

---

## Instalação

1. Acesse a [última release](https://github.com/brunoflma/claude-gateway/releases/latest) e baixe o arquivo `claude-gateway-v*.zip`
2. Extraia o conteúdo na pasta do seu sistema:
   - **Windows:** `C:\Users\SEU_USUARIO\.office-addin-dev-certs\`
   - **macOS:** `~/.office-addin-dev-certs/`
3. Instale o certificado SSL (`localhost.crt`) como confiável
4. Carregue o `manifest.xml` via Office Online (Word/Excel/PowerPoint)
5. Abra o guia `00 - Comece Aqui.html` para instruções detalhadas

---

## Estrutura

```
.office-addin-dev-certs/
├── 00 - Comece Aqui.html    ← Guia de instalação
├── Claude Gateway.vbs       ← Lançador (Windows)
├── localhost.crt             ← Certificado SSL
├── manifest.xml              ← Manifesto do Add-in
└── .app/                     ← Pasta oculta (não modificar)
    ├── proxy-cors.js
    ├── gateway_gui.py
    ├── gateway-config.json
    ├── node/                 ← Node.js embutido
    └── python/               ← Python embutido
```

---

## Modelos e Modos de Operação

### Modo Gratuito (padrão)

| Modelo no Add-in | Modelo real via ZenMux |
|---|---|
| Claude Opus 4.7 | deepseek-v4-pro-free |
| Claude Opus 4.6 | deepseek-v4-pro-free |
| Claude Sonnet 4.6 | deepseek-v4-flash-free |

### Modo Pago

Use créditos ZenMux para acessar os modelos Claude reais (Opus, Sonnet, Haiku).

---

## Solução de Problemas

| Erro | Solução |
|---|---|
| "Could not retrieve the model list" | O proxy não está ativo. Inicie pelo `Claude Gateway.vbs` |
| "The connection timed out" | Rate limit do modelo gratuito. Aguarde ~30s |
| Certificado não confiável | Reinstale o `localhost.crt` como confiável |

### Logs de diagnóstico

- **Windows:** `Get-Content "$env:USERPROFILE\.office-addin-dev-certs\.app\logs\proxy.log" -Tail 30`
- **macOS:** `tail -30 ~/.office-addin-dev-certs/.app/logs/proxy.log`

---

Desenvolvido por **Bruno Ferreira** — 2026
