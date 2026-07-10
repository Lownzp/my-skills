# Common FlClash Rules

Use precise rules first. Broaden only after repeated evidence that related domains fail.

## OpenAI and ChatGPT

```text
DOMAIN-SUFFIX,openai.com,YKKCLOUD
DOMAIN-SUFFIX,chatgpt.com,YKKCLOUD
DOMAIN-SUFFIX,oaistatic.com,YKKCLOUD
DOMAIN-SUFFIX,oaiusercontent.com,YKKCLOUD
```

## Flutter and Google Storage

Start precise:

```text
DOMAIN,storage.googleapis.com,YKKCLOUD
```

Broaden only if other Google API hosts fail:

```text
DOMAIN-SUFFIX,googleapis.com,YKKCLOUD
DOMAIN-SUFFIX,gstatic.com,YKKCLOUD
```

Do not change the FlClash node test URL to OpenAI endpoints; OpenAI can return 401/403 and mislead url-test groups.

## GitHub

```text
DOMAIN-SUFFIX,github.com,YKKCLOUD
DOMAIN-SUFFIX,githubusercontent.com,YKKCLOUD
DOMAIN-SUFFIX,githubassets.com,YKKCLOUD
```

## npm and Node

```text
DOMAIN-SUFFIX,npmjs.org,YKKCLOUD
DOMAIN-SUFFIX,npmjs.com,YKKCLOUD
DOMAIN-SUFFIX,nodejs.org,YKKCLOUD
```

## Maven and Gradle

```text
DOMAIN-SUFFIX,maven.org,YKKCLOUD
DOMAIN-SUFFIX,maven.apache.org,YKKCLOUD
DOMAIN-SUFFIX,repo.maven.apache.org,YKKCLOUD
DOMAIN-SUFFIX,plugins.gradle.org,YKKCLOUD
DOMAIN-SUFFIX,services.gradle.org,YKKCLOUD
```
