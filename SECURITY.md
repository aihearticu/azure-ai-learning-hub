# Security Policy

## 🔒 Security Best Practices

This repository is designed for educational purposes. When using the labs and examples:

### 1. Credential Management

**NEVER commit credentials to the repository:**
- API keys
- Connection strings  
- Passwords
- Certificates
- Access tokens

**Always use:**
- Environment variables (`.env` files locally)
- Azure Key Vault for production
- Managed identities where possible
- GitHub Secrets for CI/CD

### 2. Resource Security

When creating Azure resources:
- Use least privilege access
- Enable network restrictions
- Implement authentication properly
- Monitor resource usage
- Set up cost alerts

### 3. Code Security

- Validate all inputs
- Handle errors gracefully
- Don't log sensitive data
- Use HTTPS for all API calls
- Keep dependencies updated

## 🚨 Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. Email details to: [security contact email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work on a fix.

## 🛡️ Security Checklist for Labs

Before submitting new labs, ensure:

- [ ] No hardcoded credentials
- [ ] `.env.example` used for configuration templates
- [ ] Sensitive data patterns added to `.gitignore`
- [ ] Input validation demonstrated
- [ ] Error handling implemented
- [ ] Security considerations documented
- [ ] Cleanup instructions provided

## 📋 Azure Security Resources

- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/fundamentals/best-practices-and-patterns)
- [Azure AI Services Security](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-security)
- [Azure Key Vault](https://docs.microsoft.com/azure/key-vault/)
- [Managed Identities](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/)

## 🔐 Example: Secure Configuration

### Bad Practice ❌
```python
# Never do this!
api_key = "abc123def456"
client = TextAnalyticsClient(endpoint, AzureKeyCredential(api_key))
```

### Good Practice ✅
```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get from environment
api_key = os.getenv("AZURE_LANGUAGE_KEY")
if not api_key:
    raise ValueError("AZURE_LANGUAGE_KEY environment variable not set")

# Use the key
client = TextAnalyticsClient(endpoint, AzureKeyCredential(api_key))
```

## 🚀 Secure Deployment

For production deployments:

1. **Use Managed Identity**
   ```python
   from azure.identity import DefaultAzureCredential
   credential = DefaultAzureCredential()
   ```

2. **Store secrets in Key Vault**
   ```python
   from azure.keyvault.secrets import SecretClient
   secret_client = SecretClient(vault_url, credential)
   api_key = secret_client.get_secret("api-key").value
   ```

3. **Implement network security**
   - Use private endpoints
   - Configure firewalls
   - Enable VNET integration

## 📊 Monitoring & Compliance

- Enable Azure Monitor
- Set up alerts for anomalies
- Review access logs regularly
- Implement data retention policies
- Follow compliance requirements (GDPR, HIPAA, etc.)

## 🔄 Regular Updates

- Review and update dependencies monthly
- Monitor Azure security advisories
- Update deprecated authentication methods
- Test security configurations regularly

---

Remember: Security is everyone's responsibility. When in doubt, ask for help!