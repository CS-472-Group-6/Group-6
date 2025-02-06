"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# TODO 1: Test Account Serialization
# - Ensure `to_dict()` correctly converts an account to a dictionary format.
# - Verify that all expected fields are included in the dictionary.

# TODO 2: Test Invalid Email Input
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.
# ===========================
# Test: Account Role Assignment
# Author: Jacob Kasbohm
# Date: 2025-02-05
# Description: Test invalid email input.
# ===========================
def validate_email():
    """Test invalid email formats that should raise a validation error."""

    # Create an account with an invalid email
    invalid_emails = [
        "not-an-email",  # Missing '@' and domain
        "spacein name@x.com", # Space in username
        "plainaddress@",  # Missing domain
        "@missingusername.com",  # Missing username
        "user@.com",  # Invalid domain part
        "user@domain,com",  # Invalid character in domain
        "user@domain..com",  # Consecutive dots in domain
        "user@domain_with_space .com"  # Spaces in domain
    ]

    for email in invalid_emails:
        account = Account(name="John Doe", email=email, role="user")
        
        # Validate email and expect DataValidationError to be raised
        with pytest.raises(DataValidationError):
            account.validate_email()  # This should raise an error for invalid emails

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.

# TODO 4: Test Positive Deposit
# - Ensure `deposit()` correctly increases the account balance.
# - Verify that depositing a positive amount updates the balance correctly.

# TODO 5: Test Deposit with Zero/Negative Values
# - Ensure `deposit()` raises an error for zero or negative amounts.
# - Verify that balance remains unchanged after an invalid deposit attempt.

# ===========================
# Test: Valid Withdrawal
# Author: Daniel Levy
# Date: 2025-02-04
# Description: Ensure `withdraw()` correctly decreases the account balance.
#              Verify that withdrawals within available balance succeed.
# ===========================
def test_valid_withdrawal():
    # Create new account for unit test
    account = Account(name="Daniel Levy", email="levyd1@unlv.nevada.edu", balance=100.00)

    # First Test: Withdraw decreases balance by the correct amount
    original_balance = account.balance
    account.withdraw(20)
    assert account.balance == (original_balance-20)
    
    # Second Test: Withdraw is able to succeed with current available balance
    original_balance = account.balance 
    amount_to_decrease_balance = 30
    account.withdraw(amount_to_decrease_balance)
    assert account.balance > amount_to_decrease_balance
    
       
# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.

