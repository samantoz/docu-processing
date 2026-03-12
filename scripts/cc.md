
### Open Router + Claude Code
## Step 1: Get Free OpenRouter Key
1. Go to `openrouter.ai/keys`
2. Create key and name it as per your need
3. Copy the key and save above

## Step 2: Install tools

```
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```
## Check claude installation
Claude Code is the agent here and the Router is acting as the translator (ccr). The tool is called claude-code-router (ccr). It's open source. Claude Code talks to a local router running on port 3456. The router translates Claude’s requests into whatever format the backend model expects.
``` 
claude --version
ccr --version
```
## Create the config file
## This tells the router which models to use and for what purpose.
- default: everyday coding model
- think: complex reasoning task
- longContext: handles big files

```
~\.claude-code-router\config.json
```
## Step 4: Set up Your API Key Permanently

```
echo 'export OPENROUTER_API_KEY="YOUR_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc

echo 'export OPENROUTER_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc

# Power shell (Administrator)
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'YOUR_KEY_HERE', 'User')
```
