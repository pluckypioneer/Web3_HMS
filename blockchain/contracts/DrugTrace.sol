// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title DrugTrace
 * @dev Smart contract for tracking high-value medical supplies and drugs
 * @author Web3 HMS Team
 */
contract DrugTrace {
    struct SupplyItem {
        string itemId;
        string name;
        string specification;
        string manufacturer;
        string batchNumber;
        uint256 productionDate;
        uint256 expiryDate;
        string currentLocation;
        address currentOwner;
        bool isActive;
        string category; // "DRUG", "MEDICAL_DEVICE", "CONSUMABLE"
    }

    struct TraceRecord {
        string itemId;
        address from;
        address to;
        string location;
        uint256 timestamp;
        string action; // "PRODUCTION", "TRANSFER", "USE", "DISPOSAL"
        string notes;
        string transactionHash; // For external verification
    }

    // Mapping from item ID to supply item
    mapping(string => SupplyItem) public supplyItems;
    
    // Mapping from item ID to trace records
    mapping(string => TraceRecord[]) public traceRecords;
    
    // Array to store all item IDs
    string[] public itemIds;
    
    // Events
    event ItemCreated(string indexed itemId, string name, string manufacturer, string batchNumber);
    event ItemTransferred(string indexed itemId, address indexed from, address indexed to, string location);
    event ItemUsed(string indexed itemId, address indexed user, string patientId, string notes);
    event ItemDisposed(string indexed itemId, address indexed disposer, string reason);

    // Modifiers
    modifier onlyValidItem(string memory itemId) {
        require(bytes(supplyItems[itemId].itemId).length > 0, "Item does not exist");
        _;
    }

    modifier onlyActiveItem(string memory itemId) {
        require(supplyItems[itemId].isActive, "Item is not active");
        _;
    }

    modifier onlyCurrentOwner(string memory itemId) {
        require(supplyItems[itemId].currentOwner == msg.sender, "Only current owner can perform this action");
        _;
    }

    /**
     * @dev Create a new supply item
     * @param itemId Unique identifier for the item
     * @param name Item name
     * @param specification Item specification
     * @param manufacturer Manufacturer address/name
     * @param batchNumber Batch number
     * @param productionDate Production timestamp
     * @param expiryDate Expiry timestamp
     * @param category Item category
     */
    function createItem(
        string memory itemId,
        string memory name,
        string memory specification,
        string memory manufacturer,
        string memory batchNumber,
        uint256 productionDate,
        uint256 expiryDate,
        string memory category
    ) external {
        require(bytes(itemId).length > 0, "Item ID cannot be empty");
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(manufacturer).length > 0, "Manufacturer cannot be empty");
        require(bytes(batchNumber).length > 0, "Batch number cannot be empty");
        require(productionDate > 0, "Production date must be valid");
        require(expiryDate > productionDate, "Expiry date must be after production date");
        require(bytes(supplyItems[itemId].itemId).length == 0, "Item already exists");

        supplyItems[itemId] = SupplyItem({
            itemId: itemId,
            name: name,
            specification: specification,
            manufacturer: manufacturer,
            batchNumber: batchNumber,
            productionDate: productionDate,
            expiryDate: expiryDate,
            currentLocation: "",
            currentOwner: msg.sender,
            isActive: true,
            category: category
        });

        itemIds.push(itemId);

        // Create initial trace record
        traceRecords[itemId].push(TraceRecord({
            itemId: itemId,
            from: address(0),
            to: msg.sender,
            location: "",
            timestamp: block.timestamp,
            action: "PRODUCTION",
            notes: "Item created by manufacturer",
            transactionHash: ""
        }));

        emit ItemCreated(itemId, name, manufacturer, batchNumber);
    }

    /**
     * @dev Transfer item to another owner
     * @param itemId Item identifier
     * @param to New owner address
     * @param location New location
     * @param notes Transfer notes
     */
    function transferItem(
        string memory itemId,
        address to,
        string memory location,
        string memory notes
    ) external onlyValidItem(itemId) onlyActiveItem(itemId) onlyCurrentOwner(itemId) {
        require(to != address(0), "Cannot transfer to zero address");
        require(to != msg.sender, "Cannot transfer to self");

        address previousOwner = supplyItems[itemId].currentOwner;
        
        supplyItems[itemId].currentOwner = to;
        supplyItems[itemId].currentLocation = location;

        // Create trace record
        traceRecords[itemId].push(TraceRecord({
            itemId: itemId,
            from: previousOwner,
            to: to,
            location: location,
            timestamp: block.timestamp,
            action: "TRANSFER",
            notes: notes,
            transactionHash: ""
        }));

        emit ItemTransferred(itemId, previousOwner, to, location);
    }

    /**
     * @dev Record item usage
     * @param itemId Item identifier
     * @param patientId Patient identifier
     * @param notes Usage notes
     */
    function useItem(
        string memory itemId,
        string memory patientId,
        string memory notes
    ) external onlyValidItem(itemId) onlyActiveItem(itemId) onlyCurrentOwner(itemId) {
        require(bytes(patientId).length > 0, "Patient ID cannot be empty");
        require(block.timestamp <= supplyItems[itemId].expiryDate, "Item has expired");

        // Create trace record
        traceRecords[itemId].push(TraceRecord({
            itemId: itemId,
            from: msg.sender,
            to: address(0),
            location: supplyItems[itemId].currentLocation,
            timestamp: block.timestamp,
            action: "USE",
            notes: string(abi.encodePacked("Used for patient: ", patientId, ". ", notes)),
            transactionHash: ""
        }));

        emit ItemUsed(itemId, msg.sender, patientId, notes);
    }

    /**
     * @dev Dispose of an item
     * @param itemId Item identifier
     * @param reason Disposal reason
     */
    function disposeItem(
        string memory itemId,
        string memory reason
    ) external onlyValidItem(itemId) onlyActiveItem(itemId) onlyCurrentOwner(itemId) {
        require(bytes(reason).length > 0, "Disposal reason cannot be empty");

        supplyItems[itemId].isActive = false;

        // Create trace record
        traceRecords[itemId].push(TraceRecord({
            itemId: itemId,
            from: msg.sender,
            to: address(0),
            location: supplyItems[itemId].currentLocation,
            timestamp: block.timestamp,
            action: "DISPOSAL",
            notes: reason,
            transactionHash: ""
        }));

        emit ItemDisposed(itemId, msg.sender, reason);
    }

    /**
     * @dev Get supply item information
     * @param itemId Item identifier
     * @return Supply item data
     */
    function getItem(string memory itemId) 
        external 
        view 
        onlyValidItem(itemId) 
        returns (SupplyItem memory) 
    {
        return supplyItems[itemId];
    }

    /**
     * @dev Get trace records for an item
     * @param itemId Item identifier
     * @return Array of trace records
     */
    function getTraceRecords(string memory itemId) 
        external 
        view 
        onlyValidItem(itemId) 
        returns (TraceRecord[] memory) 
    {
        return traceRecords[itemId];
    }

    /**
     * @dev Get items by manufacturer
     * @param manufacturer Manufacturer name
     * @return Array of item IDs
     */
    function getItemsByManufacturer(string memory manufacturer) 
        external 
        view 
        returns (string[] memory) 
    {
        uint256 count = 0;
        
        // Count matching items
        for (uint256 i = 0; i < itemIds.length; i++) {
            if (keccak256(bytes(supplyItems[itemIds[i]].manufacturer)) == keccak256(bytes(manufacturer))) {
                count++;
            }
        }
        
        // Create result array
        string[] memory result = new string[](count);
        uint256 index = 0;
        
        for (uint256 i = 0; i < itemIds.length; i++) {
            if (keccak256(bytes(supplyItems[itemIds[i]].manufacturer)) == keccak256(bytes(manufacturer))) {
                result[index] = itemIds[i];
                index++;
            }
        }
        
        return result;
    }

    /**
     * @dev Get items by batch number
     * @param batchNumber Batch number
     * @return Array of item IDs
     */
    function getItemsByBatch(string memory batchNumber) 
        external 
        view 
        returns (string[] memory) 
    {
        uint256 count = 0;
        
        // Count matching items
        for (uint256 i = 0; i < itemIds.length; i++) {
            if (keccak256(bytes(supplyItems[itemIds[i]].batchNumber)) == keccak256(bytes(batchNumber))) {
                count++;
            }
        }
        
        // Create result array
        string[] memory result = new string[](count);
        uint256 index = 0;
        
        for (uint256 i = 0; i < itemIds.length; i++) {
            if (keccak256(bytes(supplyItems[itemIds[i]].batchNumber)) == keccak256(bytes(batchNumber))) {
                result[index] = itemIds[i];
                index++;
            }
        }
        
        return result;
    }

    /**
     * @dev Check if item is expired
     * @param itemId Item identifier
     * @return True if item is expired
     */
    function isItemExpired(string memory itemId) 
        external 
        view 
        onlyValidItem(itemId) 
        returns (bool) 
    {
        return block.timestamp > supplyItems[itemId].expiryDate;
    }

    /**
     * @dev Get total number of items
     * @return Number of items
     */
    function getTotalItems() external view returns (uint256) {
        return itemIds.length;
    }
}
