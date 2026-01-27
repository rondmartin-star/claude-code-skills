# Deployment Patterns Reference

Load this file when deploying to production with HTTPS, configuring network settings, or troubleshooting deployment issues.

---

## HTTPS Production Deployment

### Caddy Auto-Setup Pattern

```batch
REM After BASE_URL prompt in INSTALL-AND-RUN.bat:
echo !BASE_URL! | findstr "^https://" >nul
if !errorlevel! equ 0 (
    echo HTTPS detected - configuring Caddy reverse proxy...
    call :setup_caddy
)
```

### Base URL Rules

| Scenario | BASE_URL Format |
|----------|-----------------|
| Local testing | `http://localhost:8008` |
| Production HTTPS | `https://pms.ucc-austin.org` (no port) |

**HTTPS URLs must NOT include port** - Caddy handles 443 automatically.

### Network Deployment Checklist

Before declaring HTTPS deployment complete:

**Router:**
- [ ] Port 80 forwarded (Let's Encrypt validation)
- [ ] Port 443 forwarded (HTTPS traffic)
- [ ] Router admin NOT on port 443

**DNS:**
- [ ] A record → public IP (`nslookup {domain}`)

**Server:**
- [ ] Caddy listening (`netstat -an | findstr ":443"`)
- [ ] App on configured port
- [ ] Firewall allows Caddy

### Hairpin NAT Workaround

**Symptom:** External works, internal fails or shows router page.

**Fix:** Add to `C:\Windows\System32\drivers\etc\hosts`:
```
192.168.0.132    pms.ucc-austin.org
```

**Test sequence:** Phone on mobile data first → if works, internal fail = hairpin NAT.

---

## Installer Smart Defaults

Configure organization-specific defaults in INSTALL-AND-RUN.bat:

| Setting | Pattern | Example |
|---------|---------|---------|
| Response filename | `{AppName}_install_response.enc` | `UCC-PMS_install_response.enc` |
| Server port | Non-default | `8008` (not 8000) |
| Base URL | Public HTTPS | `https://pms.ucc-austin.org` |
| OAuth domain | Org domain | `ucc-austin.org` |
| SMTP sender | Service account | `PropertyManager@ucc-austin.org` |

### Directory Auto-Creation

When accepting file paths, create directories automatically:

```batch
REM Extract directory from user-provided path and create if needed
for %%F in ("!USER_PATH!") do set "DIR_PATH=%%~dpF"
if not "!DIR_PATH!"=="" if not exist "!DIR_PATH!" (
    mkdir "!DIR_PATH!" 2>nul
    if !errorlevel! equ 0 echo Created directory: !DIR_PATH!
)
```

### Response File Path Handling

```batch
set "DEFAULT_RESPONSE=%USERPROFILE%\Documents\%APP_NAME%_install_response.enc"
set /p RESPONSE_PATH="Response file path [%DEFAULT_RESPONSE%]: "
if "!RESPONSE_PATH!"=="" set "RESPONSE_PATH=%DEFAULT_RESPONSE%"

REM Auto-create directory for response file
for %%F in ("!RESPONSE_PATH!") do set "RESP_DIR=%%~dpF"
if not "!RESP_DIR!"=="" if not exist "!RESP_DIR!" mkdir "!RESP_DIR!" 2>nul
```

---

## Error Documentation Format

Document bugs in `docs/ERROR-AND-FIXES-LOG.md`:

```markdown
### Error N: [Brief Title]
**Error**: [message]
**Symptoms**: [observable issues]
**Root Cause**: [why]
**Fix**: [what changed]
**Prevention**: [how to avoid]
```

**For detailed example entries and templates:**
```
~/.claude/skills/windows-app/windows-app-build/references/templates.md
```

---

## Troubleshooting Deployment

### HTTPS Not Working

**Check sequence:**
1. DNS resolves to public IP: `nslookup yourdomain.com`
2. Port 80/443 forwarded on router
3. Caddy running: `netstat -an | findstr ":443"`
4. Firewall allows Caddy
5. Certificate obtained: Check Caddy logs
6. App running on configured port

**Common issues:**
- Router admin on port 443 → Move to different port
- ISP blocks port 80 → Contact ISP
- DNS not propagated → Wait 24-48 hours
- Firewall blocking → Add Caddy exception

### Internal Access Issues

**Hairpin NAT not supported:**
- External URL works fine
- Internal users see router admin page or timeout
- Fix: Add hosts file entry for internal IP

**Verify:**
1. Test from mobile data (external network)
2. If works externally but not internally → Hairpin NAT issue
3. Add hosts entry: `192.168.x.x yourdomain.com`

### Let's Encrypt Certificate Issues

**"Unable to obtain certificate":**
- Port 80 not forwarded → Forward port 80
- DNS not pointing to public IP → Fix DNS
- Domain contains underscores → Use hyphens
- Too many cert requests → Wait 1 week

**Certificate renewal failures:**
- Check Caddy logs: `caddy log`
- Verify port 80 still forwarded
- Restart Caddy service
- Manual renewal: `caddy reload`

---

## Production Deployment Workflow

### Pre-Deployment

1. **Test locally:** Full smoke test on localhost
2. **Backup current version:** Save working package
3. **Document changes:** Update CHANGELOG.md
4. **Security audit:** Run security checklist
5. **Database backup:** Backup production DB

### Deployment Steps

1. **Stop current service:** `nssm stop AppName`
2. **Backup database:** Copy SQLite file
3. **Replace files:** Update application files
4. **Database migration:** Run any ALTER TABLE statements
5. **Test startup:** `python -m app.main` manually
6. **Start service:** `nssm start AppName`
7. **Verify:** Check health endpoint, smoke test

### Post-Deployment

1. **Monitor logs:** Check for errors
2. **Test critical paths:** Auth, forms, DB operations
3. **Verify HTTPS:** Certificate valid, secure connections
4. **User acceptance:** Notify users, gather feedback
5. **Document issues:** Log any problems encountered

### Rollback Procedure

If deployment fails:

1. **Stop new service:** `nssm stop AppName`
2. **Restore previous version:** Copy backup files back
3. **Restore database:** Copy backup SQLite file
4. **Start service:** `nssm start AppName`
5. **Verify:** Confirm old version working
6. **Investigate:** Determine root cause before retry

---

## Production Environment Best Practices

### Configuration

- Use environment-specific settings
- Store secrets in encrypted response file
- Log to files (not console)
- Enable error monitoring
- Configure health checks

### Security

- HTTPS only (no HTTP in production)
- Secure cookie flags set
- Content Security Policy headers
- Regular security updates
- Access logs enabled

### Monitoring

- Health check endpoint: `/health`
- Application logs: Review daily
- Error rate alerts: Set thresholds
- Disk space monitoring: Alert at 80%
- Certificate expiry: Alert 30 days before

### Maintenance

- Regular backups: Daily automated
- Update schedule: Monthly security patches
- Version control: Tag releases
- Documentation: Keep deployment docs current
- Disaster recovery plan: Test annually

---

*End of Deployment Patterns Reference*
