const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying Web3 HMS Smart Contracts...");

  // Get the contract factories
  const MedicalRecordHash = await ethers.getContractFactory("MedicalRecordHash");
  const AccessControl = await ethers.getContractFactory("AccessControl");
  const DrugTrace = await ethers.getContractFactory("DrugTrace");

  // Deploy contracts
  console.log("Deploying MedicalRecordHash contract...");
  const medicalRecordHash = await MedicalRecordHash.deploy();
  await medicalRecordHash.waitForDeployment();
  const medicalRecordHashAddress = await medicalRecordHash.getAddress();
  console.log("MedicalRecordHash deployed to:", medicalRecordHashAddress);

  console.log("Deploying AccessControl contract...");
  const accessControl = await AccessControl.deploy();
  await accessControl.waitForDeployment();
  const accessControlAddress = await accessControl.getAddress();
  console.log("AccessControl deployed to:", accessControlAddress);

  console.log("Deploying DrugTrace contract...");
  const drugTrace = await DrugTrace.deploy();
  await drugTrace.waitForDeployment();
  const drugTraceAddress = await drugTrace.getAddress();
  console.log("DrugTrace deployed to:", drugTraceAddress);

  // Save deployment info
  const deploymentInfo = {
    network: network.name,
    timestamp: new Date().toISOString(),
    contracts: {
      MedicalRecordHash: {
        address: medicalRecordHashAddress,
        abi: MedicalRecordHash.interface.format("json")
      },
      AccessControl: {
        address: accessControlAddress,
        abi: AccessControl.interface.format("json")
      },
      DrugTrace: {
        address: drugTraceAddress,
        abi: DrugTrace.interface.format("json")
      }
    }
  };

  // Write deployment info to file
  const fs = require('fs');
  const path = require('path');
  const deploymentPath = path.join(__dirname, '..', 'deployments', `${network.name}.json`);
  
  // Create deployments directory if it doesn't exist
  const deploymentsDir = path.dirname(deploymentPath);
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }
  
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`Deployment info saved to: ${deploymentPath}`);

  console.log("\n=== Deployment Summary ===");
  console.log("Network:", network.name);
  console.log("MedicalRecordHash:", medicalRecordHashAddress);
  console.log("AccessControl:", accessControlAddress);
  console.log("DrugTrace:", drugTraceAddress);
  console.log("========================\n");

  // Verify contracts on Etherscan if not on local network
  if (network.name !== "hardhat" && network.name !== "localhost") {
    console.log("Waiting for block confirmations before verification...");
    await new Promise(resolve => setTimeout(resolve, 30000));

    try {
      console.log("Verifying MedicalRecordHash contract...");
      await hre.run("verify:verify", {
        address: medicalRecordHashAddress,
        constructorArguments: [],
      });

      console.log("Verifying AccessControl contract...");
      await hre.run("verify:verify", {
        address: accessControlAddress,
        constructorArguments: [],
      });

      console.log("Verifying DrugTrace contract...");
      await hre.run("verify:verify", {
        address: drugTraceAddress,
        constructorArguments: [],
      });

      console.log("All contracts verified successfully!");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
