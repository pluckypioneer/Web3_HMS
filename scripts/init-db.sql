-- Web3 HMS Database Initialization Script
-- This script creates the initial database schema and sample data

-- Create database if not exists (handled by POSTGRES_DB environment variable)
-- CREATE DATABASE hms_db;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create departments table
CREATE TABLE IF NOT EXISTS departments (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample departments
INSERT INTO departments (id, name, description) VALUES
('CARDIO', '心血管内科', '心血管疾病诊疗'),
('NEURO', '神经内科', '神经系统疾病诊疗'),
('ORTHO', '骨科', '骨科疾病诊疗'),
('PEDIA', '儿科', '儿童疾病诊疗'),
('EMERG', '急诊科', '急诊医疗服务'),
('SURG', '外科', '外科手术治疗')
ON CONFLICT (id) DO NOTHING;

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'patient',
    blockchain_addr VARCHAR(42),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_id_card ON patients(id_card);
CREATE INDEX IF NOT EXISTS idx_patients_medical_card_id ON patients(medical_card_id);
CREATE INDEX IF NOT EXISTS idx_patients_blockchain_addr ON patients(blockchain_addr);
CREATE INDEX IF NOT EXISTS idx_doctors_license_no ON doctors(license_no);
CREATE INDEX IF NOT EXISTS idx_doctors_dept_id ON doctors(dept_id);
CREATE INDEX IF NOT EXISTS idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_schedule_time ON appointments(schedule_time);
CREATE INDEX IF NOT EXISTS idx_emr_records_patient_id ON emr_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_emr_records_doctor_id ON emr_records(doctor_id);
CREATE INDEX IF NOT EXISTS idx_emr_records_blockchain_tx_hash ON emr_records(blockchain_tx_hash);
CREATE INDEX IF NOT EXISTS idx_data_hashes_original_id ON data_hashes(original_id);
CREATE INDEX IF NOT EXISTS idx_data_hashes_tx_hash ON data_hashes(tx_hash);
CREATE INDEX IF NOT EXISTS idx_access_grants_grantor_addr ON access_grants(grantor_addr);
CREATE INDEX IF NOT EXISTS idx_access_grants_grantee_addr ON access_grants(grantee_addr);

-- Insert sample users
INSERT INTO users (email, password_hash, name, role, blockchain_addr) VALUES
('admin@hms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4VqJqJqJqJ', '系统管理员', 'admin', '0x1234567890123456789012345678901234567890'),
('doctor1@hms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4VqJqJqJqJ', '张医生', 'doctor', '0x2345678901234567890123456789012345678901'),
('doctor2@hms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4VqJqJqJqJ', '李医生', 'doctor', '0x3456789012345678901234567890123456789012'),
('patient1@hms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4VqJqJqJqJ', '王患者', 'patient', '0x4567890123456789012345678901234567890123')
ON CONFLICT (email) DO NOTHING;

-- Insert sample doctors
INSERT INTO doctors (name, title, dept_id, dept_name, license_no, phone, email, specialization, blockchain_addr) VALUES
('张医生', '主任医师', 'CARDIO', '心血管内科', 'DOC001', '13800138001', 'doctor1@hms.com', '心血管疾病诊疗', '0x2345678901234567890123456789012345678901'),
('李医生', '副主任医师', 'NEURO', '神经内科', 'DOC002', '13800138002', 'doctor2@hms.com', '神经系统疾病诊疗', '0x3456789012345678901234567890123456789012')
ON CONFLICT (license_no) DO NOTHING;

-- Insert sample patients
INSERT INTO patients (name, id_card, phone, email, birth_date, gender, medical_card_id, blockchain_addr, insurance_type) VALUES
('王患者', '110101199001011234', '13900139001', 'patient1@hms.com', '1990-01-01', '男', 'MC001', '0x4567890123456789012345678901234567890123', '城镇职工医保'),
('李患者', '110101199002021234', '13900139002', 'patient2@hms.com', '1990-02-02', '女', 'MC002', '0x5678901234567890123456789012345678901234', '城镇居民医保')
ON CONFLICT (id_card) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_doctors_updated_at BEFORE UPDATE ON doctors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_emr_records_updated_at BEFORE UPDATE ON emr_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_inpatients_updated_at BEFORE UPDATE ON inpatients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_drugs_updated_at BEFORE UPDATE ON drugs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_contracts_updated_at BEFORE UPDATE ON contracts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_data_hashes_updated_at BEFORE UPDATE ON data_hashes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_access_grants_updated_at BEFORE UPDATE ON access_grants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hms_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hms_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO hms_user;
