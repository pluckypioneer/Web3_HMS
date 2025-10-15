# Web3 Hospital Management System (Web3 HMS)

DOCUMENT:[Chinese中文](https://github.com/pluckypioneer/Web3_HMS/blob/main/README_zh.md)、[English](https://github.com/pluckypioneer/Web3_HMS/blob/main/README.md)

> 一个人写这个有点太难了，用ai有时候还帮倒忙，越写越觉得是屎山，有愿意接手的我很乐意转让这个repo，要是有人愿意跟我合作我也很开心，谢谢！

A modern hospital management system based on blockchain technology, integrating Solidity, Vue 3, and Flask technology stacks to achieve tamper-proof medical data storage, full-process digital management, and multi-role collaborative work.

> 📌 **Project Status**: Core functionality development completed, ready for normal operation.

## 🚀 Project Features

- **🔗 Blockchain Integration**: Medical data hash storage to ensure data integrity and immutability
- **🏥 Medical Professionalism**: Covers core scenarios such as patient services, clinical diagnosis and treatment, inpatient management, and pharmaceutical supplies
- **🔐 Data Security**: RBAC-based permission control, supporting fine-grained data access management
- **📱 Modern UI**: Vue 3 + Element Plus, responsive design, multi-device adaptation
- **🐳 Containerized Deployment**: Docker containerization, supporting one-click deployment and scaling
- **📊 Real-time Monitoring**: Blockchain status monitoring, system health checks

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Layer                             │
├─────────────────────────────────────────────────────────────┤
│  Patient End (Web/H5)  │  Medical Staff End (Web)  │  Admin End (Web)  │  Operation End (Web) │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Layer (Vue 3)                    │
├─────────────────────────────────────────────────────────────┤
│  Element Plus UI  │  Vue Router  │  Pinia State Management  │  Web3.js  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway Layer (Flask)                  │
├─────────────────────────────────────────────────────────────┤
│  JWT Authentication  │  RBAC Permissions  │  Request Throttling  │  CORS Handling  │  Logging  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│               Business Logic Layer (Flask)                  │
├─────────────────────────────────────────────────────────────┤
│ Patient Services │ Clinical Diagnosis │ Inpatient Management │ Pharmaceutical Supplies │ Operation Management │ Statistical Analysis │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                           │
├─────────────────────────────────────────────────────────────┤
│ PostgreSQL │ Redis Cache │ Blockchain │ IPFS Storage │ File System │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Frontend Technology
- **Vue 3**: Progressive JavaScript framework
- **Element Plus**: Vue 3 component library
- **Vue Router**: Official routing manager
- **Pinia**: State management library
- **Web3.js**: Blockchain interaction library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Modern build tool

### Backend Technology
- **Flask**: Lightweight Python Web framework
- **Flask-RESTful**: RESTful API development
- **SQLAlchemy**: Python ORM
- **PostgreSQL**: Relational database
- **Redis**: In-memory database
- **JWT**: Identity authentication
- **Celery**: Asynchronous task queue

### Blockchain Technology
- **Solidity**: Smart contract development language
- **Hardhat**: Ethereum development environment
- **Web3.js**: Frontend blockchain interaction
- **IPFS**: Decentralized file storage

### Deployment & Operations
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy server
- **Gunicorn**: WSGI HTTP server

## 📋 Core Features

### Patient Service Module
- ✅ Multi-channel appointment registration
- ✅ Electronic medical card management
- ✅ Medical record inquiry (for self)
- ✅ Medical insurance settlement
- ✅ Examination report viewing

### Clinical Diagnosis Module
- ✅ Electronic medical record entry
- ✅ Medical order management
- ✅ Prescription issuance and review
- ✅ Examination and test application
- ✅ Surgery and anesthesia management

### Inpatient Management Module
- ✅ Bed allocation and management
- ✅ Real-time calculation of inpatient expenses
- ✅ Discharge settlement
- ✅ Nursing plans and records

### Pharmaceutical & Supplies Module
- ✅ Drug inventory management
- ✅ High-value consumable traceability
- ✅ Consumable requisition and verification

### Blockchain Features
- ✅ Medical data hash storage
- ✅ Data access permission control
- ✅ Pharmaceutical supply chain traceability
- ✅ Data integrity verification

## 🚀 Quick Start

### Environment Requirements

- **Node.js**: >= 18.0.0
- **Python**: >= 3.9
- **Docker**: >= 20.10.0
- **Docker Compose**: >= 2.0.0
- **Git**: >= 2.30.0

### One-click Deployment

1. **Clone the project**
```bash
git clone https://github.com/pluckypioneer/Web3_HMS
cd Web3_HMS
```

2. **Configure environment variables**
```bash
# Copy environment configuration file
cp env.example .env

# Modify configuration according to actual environment
vim .env
```

3. **Start services**
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

4. **Access the system**
- Frontend interface: http://localhost:3000
- Backend API: http://localhost:5000
- Blockchain node: http://localhost:8545
- IPFS node: http://localhost:5001

### Default Accounts

| Role | Email | Password | Description |
|------|------|------|------|
| Administrator | admin@hms.com | password123 | System administrator |
| Doctor | doctor1@hms.com | password123 | Dr. Zhang |
| Patient | patient1@hms.com | password123 | Patient Wang |

### API and Database Configuration Items That Require Manual Setup

Relevant environment variables need to be configured before the system runs, mainly including:

1. **Database Configuration**
   - `DATABASE_URL`: Database connection string for production environment
   - `DEV_DATABASE_URL`: Database connection string for development environment
   - `TEST_DATABASE_URL`: Database connection string for test environment

2. **Security Key Configuration**
   - `SECRET_KEY`: Flask application key
   - `JWT_SECRET_KEY`: JWT authentication key

3. **Blockchain Configuration**
   - `WEB3_PROVIDER_URL`: Blockchain node URL
   - `MEDICAL_RECORD_HASH_ADDRESS`: Medical record hash contract address
   - `ACCESS_CONTROL_ADDRESS`: Access control contract address
   - `DRUG_TRACE_ADDRESS`: Drug traceability contract address

4. **Email Service Configuration**
   - `MAIL_SERVER`: Email server address
   - `MAIL_PORT`: Email server port
   - `MAIL_USERNAME`: Email username
   - `MAIL_PASSWORD`: Email password or application-specific password

5. **Other Configurations**
   - `CORS_ORIGINS`: List of cross-origin access sources
   - `IPFS_URL`: IPFS node URL

For complete configuration items, please refer to the [env.example](env.example) file.

## 🔧 Development Guide

### Local Development Environment

1. **Start database services**
```bash
docker-compose up postgres redis ipfs ganache -d
```

2. **Start backend service**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

3. **Start frontend service**
```bash
cd frontend
npm install
npm run dev
```

4. **Deploy smart contracts**
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### Project Structure

```
Web3_HMS/
├── frontend/                 # Vue 3 frontend
│   ├── src/
│   │   ├── components/       # Components
│   │   ├── views/            # Pages
│   │   ├── stores/           # State management
│   │   ├── router/           # Routing configuration
│   │   ├── utils/            # Utility functions
│   │   ├── App.vue           # Root component
│   │   ├── main.ts           # Entry file
│   │   └── style.css         # Global styles
│   ├── package.json          # Frontend dependency configuration
│   ├── vite.config.ts        # Vite configuration
│   ├── tsconfig.json         # TypeScript configuration
│   └── index.html            # HTML template
├── backend/                  # Flask backend
│   ├── api/                 # API routes
│   │   ├── resources/       # Resource definitions
│   │   └── __init__.py      # API initialization
│   ├── models/              # Data models
│   ├── config.py            # Configuration file
│   ├── app.py               # Application entry
│   ├── extensions.py         # Extension modules
│   └── requirements.txt     # Backend dependency configuration
├── blockchain/               # Smart contracts
│   ├── contracts/           # Solidity contracts
│   ├── scripts/             # Deployment scripts
│   ├── hardhat.config.js    # Hardhat configuration
│   └── package.json         # Blockchain dependency configuration
├── nginx/                   # Nginx configuration
│   └── nginx.conf           # Nginx configuration file
├── scripts/                 # Script files
│   ├── init-db.sql          # Database initialization script
│   ├── setup.bat            # Windows installation script
│   └── setup.sh             # Linux/Mac installation script
├── docker-compose.yml       # Docker orchestration
├── env.example              # Environment variable example
└── README.md
```

## 🔐 Security Features

### Data Security
- **Transmission Encryption**: Full-interface HTTPS encryption
- **Storage Encryption**: Encrypted storage of sensitive data
- **Access Control**: RBAC-based fine-grained permission management
- **Audit Logs**: Complete operation audit tracking

### Blockchain Security
- **Smart Contract Auditing**: Mythril, Slither security scanning
- **Hash Verification**: SHA-256 data integrity verification
- **Permission Management**: Blockchain address-based access control
- **Immutability**: Permanent storage of medical data hashes

### Compliance
- **Medical Data Compliance**: Compliant with "Electronic Medical Record Application Management Specifications"
- **Privacy Protection**: In line with "Personal Information Protection Law"
- **Blockchain Compliance**: Meets judicial evidence storage standards

## 📊 Monitoring and Operations

### Health Check
```bash
# Check service status
curl http://localhost:5000/health

# Check blockchain connection
curl http://localhost:5000/api/blockchain/status
```

### Log Viewing
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Data Backup
```bash
# Backup database
docker-compose exec postgres pg_dump -U hms_user hms_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U hms_user hms_db < backup.sql
```

## 🚀 Deployment Guide

### Production Environment Deployment

1. **Environment Configuration**
```bash
# Copy environment configuration file
cp .env.example .env

# Modify production environment configuration
vim .env
```

2. **SSL Certificate Configuration**
```bash
# Generate SSL certificate (development environment)
openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes

# Modify nginx.conf to enable HTTPS
```

3. **Start Production Services**
```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose ps
```

### Scaling Deployment

```bash
# Horizontally scale backend services
docker-compose up -d --scale backend=3

# Add load balancing
docker-compose up -d nginx
```

## 🤝 Contribution Guide

1. **Fork the project**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push the branch**: `git push origin feature/AmazingFeature`
5. **Submit a Pull Request**

### Local Development

It is recommended to use VS Code for development; the project has a pre-configured debugging environment.

### Development Specifications

- **Code Style**: Follow ESLint and Prettier configurations
- **Commit Messages**: Use Conventional Commits specifications
- **Test Coverage**: Ensure new features have corresponding test cases
- **Documentation Updates**: Timely update relevant documentation
- **Type Safety**: Use TypeScript to provide type safety guarantees

## 📝 Changelog

### v1.1.0 (2025-09-25)
- ✅ Fixed missing frontend components
- ✅ Improved user authentication system
- ✅ Optimized system architecture and code structure
- ✅ Fixed multiple TypeScript type errors
- ✅ Cleaned up redundant files and code

### v1.0.0 (2025-09-13)
- ✅ Initial version release
- ✅ Core functional modules completed
- ✅ Blockchain integration completed
- ✅ Docker containerized deployment
- ✅ Basic security protection

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/pluckypioneer/Web3_HMS/blob/main/LICENSE) file for details.

## 🆘 Support and Help

### Frequently Asked Questions

**Q: How to reset the administrator password?**
A: Directly modify the password_hash field in the users table through the database.

**Q: What to do if a blockchain transaction fails?**
A: Check if the Ganache node is running normally and ensure the account has sufficient balance.

**Q: How to add a new department?**
A: Insert a new record in the departments table or add it through the management interface.

### Contact Information

- **Project Homepage**: [GitHub Repository](https://github.com/pluckypioneer/Web3_HMS)
- **Issue Reporting**: [GitHub Issues](https://github.com/pluckypioneer/Web3_HMS/issues)
- **Technical Discussion**: [Discussion Forum]
- **Email Contact**: pluckypioneer258@proton.me

## 🙏 Acknowledgments

Thanks to the support of the following open-source projects:
- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [Element Plus](https://element-plus.org/) - Vue 3 component library
- [Flask](https://flask.palletsprojects.com/) - Python Web framework
- [Hardhat](https://hardhat.org/) - Ethereum development environment
- [Docker](https://www.docker.com/) - Containerization platform

---

**Web3 HMS** - Making medical data more secure, making hospital management smarter 🏥✨

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pluckypioneer/Web3_HMS&type=Date)](https://www.star-history.com/#pluckypioneer/Web3_HMS&Date)

## Support Me

> USDT Address：` 0x2aa1308a4ce8671870ff5984c0b9b5fbf56b597e `

<img src="https://health.john-life.sbs/images/eth.jpg" alt="图片alt" title="OKX打赏">
