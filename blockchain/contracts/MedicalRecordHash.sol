// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title MedicalRecordHash
 * @dev Smart contract for storing medical record hashes and tracking modifications
 * @author Web3 HMS Team
 */
contract MedicalRecordHash {
    struct MedicalRecord {
        string patientId;
        string doctorId;
        string recordType; // "EMR", "PRESCRIPTION", "SURGERY", "REPORT"
        string hashValue;
        uint256 timestamp;
        address creator;
        bool isActive;
    }

    struct ModificationHistory {
        string newHash;
        uint256 timestamp;
        address modifierAddress;
        string reason;
    }

    // Mapping from record ID to medical record
    mapping(string => MedicalRecord) public medicalRecords;
    
    // Mapping from record ID to modification history
    mapping(string => ModificationHistory[]) public modificationHistory;
    
    // Array to store all record IDs
    string[] public recordIds;
    
    // Events
    event RecordCreated(string indexed recordId, string patientId, string doctorId, string recordType, string hashValue);
    event RecordModified(string indexed recordId, string newHash, address modifierAddress, string reason);
    event RecordDeactivated(string indexed recordId, address deactivator);

    // Modifiers
    modifier onlyValidRecord(string memory recordId) {
        require(bytes(medicalRecords[recordId].patientId).length > 0, "Record does not exist");
        _;
    }

    modifier onlyActiveRecord(string memory recordId) {
        require(medicalRecords[recordId].isActive, "Record is not active");
        _;
    }

    /**
     * @dev Create a new medical record hash
     * @param recordId Unique identifier for the medical record
     * @param patientId Patient identifier
     * @param doctorId Doctor identifier
     * @param recordType Type of medical record
     * @param hashValue SHA-256 hash of the medical record content
     */
    function createRecord(
        string memory recordId,
        string memory patientId,
        string memory doctorId,
        string memory recordType,
        string memory hashValue
    ) external {
        require(bytes(recordId).length > 0, "Record ID cannot be empty");
        require(bytes(patientId).length > 0, "Patient ID cannot be empty");
        require(bytes(doctorId).length > 0, "Doctor ID cannot be empty");
        require(bytes(hashValue).length > 0, "Hash value cannot be empty");
        require(bytes(medicalRecords[recordId].patientId).length == 0, "Record already exists");

        medicalRecords[recordId] = MedicalRecord({
            patientId: patientId,
            doctorId: doctorId,
            recordType: recordType,
            hashValue: hashValue,
            timestamp: block.timestamp,
            creator: msg.sender,
            isActive: true
        });

        recordIds.push(recordId);

        emit RecordCreated(recordId, patientId, doctorId, recordType, hashValue);
    }

    /**
     * @dev Modify an existing medical record hash
     * @param recordId Record identifier
     * @param newHash New hash value
     * @param reason Reason for modification
     */
    function modifyRecord(
        string memory recordId,
        string memory newHash,
        string memory reason
    ) external onlyValidRecord(recordId) onlyActiveRecord(recordId) {
        require(bytes(newHash).length > 0, "New hash value cannot be empty");
        require(bytes(reason).length > 0, "Reason cannot be empty");

        // Store modification history
        modificationHistory[recordId].push(ModificationHistory({
            newHash: newHash,
            timestamp: block.timestamp,
            modifierAddress: msg.sender,
            reason: reason
        }));

        // Update the record
        medicalRecords[recordId].hashValue = newHash;
        medicalRecords[recordId].timestamp = block.timestamp;

        emit RecordModified(recordId, newHash, msg.sender, reason);
    }

    /**
     * @dev Deactivate a medical record
     * @param recordId Record identifier
     */
    function deactivateRecord(string memory recordId) 
        external 
        onlyValidRecord(recordId) 
        onlyActiveRecord(recordId) 
    {
        medicalRecords[recordId].isActive = false;
        emit RecordDeactivated(recordId, msg.sender);
    }

    /**
     * @dev Get medical record information
     * @param recordId Record identifier
     * @return Medical record data
     */
    function getRecord(string memory recordId) 
        external 
        view 
        onlyValidRecord(recordId) 
        returns (MedicalRecord memory) 
    {
        return medicalRecords[recordId];
    }

    /**
     * @dev Get modification history for a record
     * @param recordId Record identifier
     * @return Array of modification history
     */
    function getModificationHistory(string memory recordId) 
        external 
        view 
        onlyValidRecord(recordId) 
        returns (ModificationHistory[] memory) 
    {
        return modificationHistory[recordId];
    }

    /**
     * @dev Get total number of records
     * @return Number of records
     */
    function getTotalRecords() external view returns (uint256) {
        return recordIds.length;
    }

    /**
     * @dev Verify if a hash matches the current record hash
     * @param recordId Record identifier
     * @param hashToVerify Hash to verify
     * @return True if hash matches
     */
    function verifyHash(string memory recordId, string memory hashToVerify) 
        external 
        view 
        onlyValidRecord(recordId) 
        onlyActiveRecord(recordId) 
        returns (bool) 
    {
        return keccak256(bytes(medicalRecords[recordId].hashValue)) == keccak256(bytes(hashToVerify));
    }
}
