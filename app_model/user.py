#Create TXT file if it doesn't exist
if not os.path.exists(TXT_FILE):
    with open(TXT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password', 'role']) 

#hashed by using bycrpt
def generates_hash(psw):
    bytes_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_psw, salt)
    return hashed.decode('utf-8')

#validating hash vs password
def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

#user registration
def register_user():
    username = input("Enter username: ").strip() #this first line will remove any leading or trailing whitespace from the username input
    role = input("Enter role (admin/user): ").strip().lower()

    if role not in ['admin', 'user']:
        print("Invalid role. Please enter 'admin' or 'user'.")
        return
    #checking if the username is empty afer the initial strip
    if not username:
        print("Username cannot contain spaces. Please enter a valid username.")
        return

#check if the username already exists 
    with open(TXT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row ['username'] == username:
                print("Username already exists. Please choose a different username.")
                return
            
    password = input ("Enter password: ")
    hashed = generates_hash(password)

    with open(TXT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed, role])

    print(f"User '{username}' registered successfully.")


#user login 
def login_user():
    username = input("Enter username: ").strip()
   
   #check if the username exists
    user_found = False
    stored_hash = None


    with open (TXT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                user_found = True
                stored_hash = row['password']
                break 

    if not user_found:
        print("Username not found. Please register first.")
        return
    
    #Allow the user to enter password a max amount of 3 times
    max_attempts = 3

    for attempts in range(1, max_attempts + 1):
        password = input(f"Enter password attempt {attempts}/ {max_attempts}: ")


        if is_valid_hash(password, stored_hash):
            print(f"Login successful. Welcome, {username}!")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"Login attempt timestamp: {timestamp}")
            return
        #create a time stamp for the login attempts
        
    
    

        else:
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                print(f"Invalid password. You have {remaining_attempts} attempts left.")
            else:
                print("Maximum login attempts reached. Please try again later.")
                return