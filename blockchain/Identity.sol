// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UniShieldIdentity {
    address public universityAdmin;

    struct Credential {
        string studentID;
        string department;
        bool isValid;
        uint256 issueDate;
    }

    // Maps a student's wallet address to their University Credential
    mapping(address => Credential) public credentials;

    event CredentialIssued(address indexed student, string studentID);
    event CredentialRevoked(address indexed student);

    modifier onlyAdmin() {
        require(msg.sender == universityAdmin, "Only the university can perform this action");
        _;
    }

    constructor() {
        universityAdmin = msg.sender;
    }

    // Issue a new digital ID to a student
    function issueCredential(address _student, string memory _id, string memory _dept) public onlyAdmin {
        credentials[_student] = Credential(_id, _dept, true, block.timestamp);
        emit CredentialIssued(_student, _id);
    }

    // Revoke access if a threat is detected by the AI Engine
    function revokeCredential(address _student) public onlyAdmin {
        credentials[_student].isValid = false;
        emit CredentialRevoked(_student);
    }

    // Verify identity for Zero Trust access
    function isAuthorized(address _student) public view returns (bool) {
        return credentials[_student].isValid;
    }
}
