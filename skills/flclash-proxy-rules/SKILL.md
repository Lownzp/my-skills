---
name: flclash-proxy-rules
description: Diagnose Windows/FlClash proxy routing problems and safely add FlClash rules. Use when a user reports network timeouts, connection resets, Flutter/Gradle/Git/npm dependency download failures, OpenAI/ChatGPT/Codex instability, or asks to add/update/verify FlClash proxy rules, especially on this Windows setup using FlClash at 127.0.0.1:7890.
---

# FlClash Proxy Rules

## Operating Rules

Default to read-only diagnosis first. Do not edit `config.yaml` or subscription profile YAML directly unless the user explicitly asks. On this setup, `config.yaml` is generated runtime output and profile YAML can be overwritten or encoding-damaged.

Prefer the FlClash overwrite script path:

- Preferences file: `C:\Users\ADMIN\AppData\Roaming\com.follow\clash\shared_preferences.json`
- Runtime config to verify: `C:\Users\ADMIN\AppData\Roaming\com.follow\clash\config.yaml`
- Local proxy: `http://127.0.0.1:7890`
- Preferred policy group: `YKKCLOUD`

Always back up `shared_preferences.json` before changing overwrite scripts. Avoid changing DNS, TUN, test URL, nodes, or profile files unless the user specifically asks.

## Diagnosis Workflow

For a failing host, compare direct vs proxy:

```powershell
curl.exe -I --connect-timeout 8 --max-time 20 https://example.com/
curl.exe -x http://127.0.0.1:7890 -I --connect-timeout 8 --max-time 20 https://example.com/
```

Interpret results:

- Direct fails or resets, proxy succeeds: add a precise proxy rule.
- Direct succeeds, proxy fails: try another node; do not add a rule yet.
- Both fail: investigate service availability, DNS, certificate, node, or local network.
- Both succeed: treat as intermittent; avoid adding broad rules unless failures repeat.

Useful status checks:

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 7890
Select-String -Path "$env:APPDATA\com.follow\clash\config.yaml" -Pattern "example.com"
```

## Adding Rules

Use the bound overwrite script named `chatgpt` when present. The script should prepend custom rules:

```js
const main = (config) => {
  const rules = [
    "DOMAIN-SUFFIX,openai.com,YKKCLOUD",
    "DOMAIN-SUFFIX,chatgpt.com,YKKCLOUD",
    "DOMAIN-SUFFIX,oaistatic.com,YKKCLOUD",
    "DOMAIN-SUFFIX,oaiusercontent.com,YKKCLOUD",
  ];

  config.rules = [
    ...rules,
    ...(config.rules || []),
  ];

  return config;
}
```

For automated appends, use `scripts/add_flclash_rule.py`. Example:

```powershell
python C:\Users\ADMIN\.codex\skills\flclash-proxy-rules\scripts\add_flclash_rule.py DOMAIN,storage.googleapis.com,YKKCLOUD
```

After changing the overwrite script, apply it by using FlClash's UI reload/apply or by restarting FlClash only if the user accepts a brief proxy interruption.

## Verification

Verify the generated config, not only the preferences file:

```powershell
Select-String -Path "$env:APPDATA\com.follow\clash\config.yaml" -Pattern "storage.googleapis.com|openai.com"
```

Then test the route:

```powershell
curl.exe -x http://127.0.0.1:7890 -I --connect-timeout 8 --max-time 20 https://storage.googleapis.com/
```

Expected examples:

- `api.openai.com/v1/models` returning `401` without an API key means the OpenAI HTTP path works.
- `storage.googleapis.com/` returning `400` at the root path means Google Storage TLS/HTTP works.
- `Recv failure: Connection was reset` on direct access but success through proxy indicates a rule is appropriate.

## References

Read `references/common-rules.md` when choosing exact domain rules for common developer services.
