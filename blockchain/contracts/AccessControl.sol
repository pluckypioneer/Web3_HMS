// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AccessControl
 * @dev Smart contract for managing medical data access permissions
 * @author Web3 HMS Team
 */
contract AccessControl {
    struct AccessGrant {
        string dataId;
        address grantor; // Patient who grants access
        address grantee; // Healthcare provider who receives access
        uint256 grantTime;
        uint256 expireTime;
        bool isActive;
        string dataType; // "EMR", "PRESCRIPTION", "REPORT", etc.
    }

    struct AccessLog {
        address accessor;
        uint256 accessTime;
        string dataId;
        string action; // "VIEW", "MODIFY", "EXPORT"
    }

    // Mapping from grant ID to access grant
    mapping(string => AccessGrant) public accessGrants;
    
    // Mapping from patient address to their granted accesses
    mapping(address => string[]) public patientGrants;
    
    // Mapping from healthcare provider address to their received accesses
    mapping(address => string[]) public providerAccesses;
    
    // Access logs for audit trail
    AccessLog[] public accessLogs;
    
    // Array to store all grant IDs
    string[] public grantIds;
    
    // Events
    event AccessGranted(string indexed grantId, address indexed grantor, address indexed grantee, string dataId, uint256 expireTime);
    event AccessRevoked(string indexed grantId, address indexed revoker);
    event AccessUsed(string indexed grantId, address indexed accessor, string action);
    event AccessExpired(string indexed grantId);

    // Modifiers
    modifier onlyValidGrant(string memory grantId) {
        require(bytes(accessGrants[grantId].dataId).length > 0, "Grant does not exist");
        _;
    }

    modifier onlyActiveGrant(string memory grantId) {
        require(accessGrants[grantId].isActive, "Grant is not active");
        require(accessGrants[grantId].expireTime > block.timestamp, "Grant has expired");
        _;
    }

    modifier onlyGrantorOrGrantee(string memory grantId) {
        require(
            accessGrants[grantId].grantor == msg.sender || 
            accessGrants[grantId].grantee == msg.sender,
            "Only grantor or grantee can perform this action"
        );
        _;
    }

    /**
     * @dev Grant access to medical data
     * @param grantId Unique identifier for the access grant
     * @param grantee Healthcare provider address
     * @param dataId Medical data identifier
     * @param dataType Type of medical data
     * @param duration Access duration in seconds
     */
    function grantAccess(
        string memory grantId,
        address grantee,
        string memory dataId,
        string memory dataType,
        uint256 duration
    ) external {
        require(bytes(grantId).length > 0, "Grant ID cannot be empty");
        require(grantee != address(0), "Grantee address cannot be zero");
        require(bytes(dataId).length > 0, "Data ID cannot be empty");
        require(duration > 0, "Duration must be greater than 0");
        require(bytes(accessGrants[grantId].dataId).length == 0, "Grant already exists");

        uint256 expireTime = block.timestamp + duration;

        accessGrants[grantId] = AccessGrant({
            dataId: dataId,
            grantor: msg.sender,
            grantee: grantee,
            grantTime: block.timestamp,
            expireTime: expireTime,
            isActive: true,
            dataType: dataType
        });

        patientGrants[msg.sender].push(grantId);
        providerAccesses[grantee].push(grantId);
        grantIds.push(grantId);

        emit AccessGranted(grantId, msg.sender, grantee, dataId, expireTime);
    }

    /**
     * @dev Revoke access to medical data
     * @param grantId Grant identifier
     */
    function revokeAccess(string memory grantId) 
        external 
        onlyValidGrant(grantId) 
        onlyGrantorOrGrantee(grantId) 
    {
        accessGrants[grantId].isActive = false;
        emit AccessRevoked(grantId, msg.sender);
    }

    /**
     * @dev Log access to medical data
     * @param grantId Grant identifier
     * @param action Action performed
     */
    function logAccess(string memory grantId, string memory action) 
        external 
        onlyValidGrant(grantId) 
        onlyActiveGrant(grantId) 
    {
        require(accessGrants[grantId].grantee == msg.sender, "Only grantee can log access");
        require(bytes(action).length > 0, "Action cannot be empty");

        accessLogs.push(AccessLog({
            accessor: msg.sender,
            accessTime: block.timestamp,
            dataId: accessGrants[grantId].dataId,
            action: action
        }));

        emit AccessUsed(grantId, msg.sender, action);
    }

    /**
     * @dev Check if an address has access to specific data
     * @param grantId Grant identifier
     * @param accessor Address to check
     * @return True if access is granted and active
     */
    function hasAccess(string memory grantId, address accessor) 
        external 
        view 
        onlyValidGrant(grantId) 
        returns (bool) 
    {
        AccessGrant memory grant = accessGrants[grantId];
        return grant.isActive && 
               grant.expireTime > block.timestamp && 
               grant.grantee == accessor;
    }

    /**
     * @dev Get access grant information
     * @param grantId Grant identifier
     * @return Access grant data
     */
    function getAccessGrant(string memory grantId) 
        external 
        view 
        onlyValidGrant(grantId) 
        returns (AccessGrant memory) 
    {
        return accessGrants[grantId];
    }

    /**
     * @dev Get all grants for a patient
     * @param patient Patient address
     * @return Array of grant IDs
     */
    function getPatientGrants(address patient) external view returns (string[] memory) {
        return patientGrants[patient];
    }

    /**
     * @dev Get all accesses for a healthcare provider
     * @param provider Provider address
     * @return Array of grant IDs
     */
    function getProviderAccesses(address provider) external view returns (string[] memory) {
        return providerAccesses[provider];
    }

    /**
     * @dev Get access logs for audit trail
     * @param limit Maximum number of logs to return
     * @return Array of access logs
     */
    function getAccessLogs(uint256 limit) external view returns (AccessLog[] memory) {
        uint256 length = accessLogs.length;
        if (limit > length) {
            limit = length;
        }
        
        AccessLog[] memory logs = new AccessLog[](limit);
        for (uint256 i = 0; i < limit; i++) {
            logs[i] = accessLogs[length - 1 - i]; // Return most recent logs first
        }
        
        return logs;
    }

    /**
     * @dev Get total number of grants
     * @return Number of grants
     */
    function getTotalGrants() external view returns (uint256) {
        return grantIds.length;
    }

    /**
     * @dev Check if grant is expired
     * @param grantId Grant identifier
     * @return True if grant is expired
     */
    function isGrantExpired(string memory grantId) 
        external 
        view 
        onlyValidGrant(grantId) 
        returns (bool) 
    {
        return accessGrants[grantId].expireTime <= block.timestamp;
    }
}
