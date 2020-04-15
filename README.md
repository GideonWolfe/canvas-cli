# canvas-cli

![Example with wtfutil](/screenshots/wtfutil.png?raw=true "wtfutil example")

## Configuration
Go to your `Canvas Account > Settings > Approved Integrations > New Access Token` and copy your token.

Enter this into `config.yaml` with the Canvas domain you are targeting

```yaml
default: &default
  canvasdomain: ""
  canvastoken: ""
```

## Usage
`canvas-cli` is a command line tool to fetch and display basic information from your canvas account.

Here are the current working actions:

`-list`
  * `courses`
  * `assignments` `<courseid>`
 
 `summary`
