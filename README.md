# CSCCTF v6

## General Notes:
- This GitHub repository is used to upload challenge files.
- We use Notion to track progress.
- Please follow the specified folders/files structure to ensure smooth deployment.
- Focus on writing your challenge first; the `Dockerfile` should be the last step.
- Be careful when dealing with Github, dont push/merge to the main branch.
- Open pull requests when your challenge is tested by other writers only.
- For dynamic challenges get the flag from the environment variable `FLAG`.
- If you need any help contact us: @3lawneh @ava_l4nch .

## Steps to add your challenge

### ⚠️ Please dont push or merge to the main branch directly. Only Create a Pull Resquest (PR). (Be careful in steps 6 and 7)

1. Clone the repository:

   Note: You need to [authenticate](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git#authenticating-with-github-from-git) because this is a private repository.

   ```bash
   git clone -b template <repo url>
   ```

2. Create new branch:

   ```bash
   git checkout -b Category/ChallengeName
   ```

3. Add your challenge files
   ```
    📁 Category/
      └── 📁 Chall_name/
          ├── 📁 source/
          ├── 📁 handouts/
          ├── 📁 solution/
          │   └── 📄README.md
          ├── 🐳 Dockerfile
          ├── 📄 build.sh
          └── 📄 README.md
   ```
   - `source/` contains the challenge source code. (Your challenge starts here)
   - `handouts/` contains files that will be handed out to the players.
   - `solution/` contains the solution to the challenge (Scripts/Steps/Screenshots).
   - `Dockerfile` is used to build a Docker image for the challenge. (Only for challenges that require instances web/crypto/pwn/rev/misc. [Templates](#dockerfile-templates))
   - `README.md`  is used to provide information about the challenge ([Template](#readmemd-structure))

4. Add files to the commit:

   ```bash
   git add .
   ```

5. Commit changes to **local** repository:

   ```bash
   git commit -m "<commit message>"
   ```

6. Push changes to **remote** repository:

   ```bash
   git push origin <branch name>
   ```

⚠️ Here starts the testing phase, after testing is done and needed changes are made, you can do step 7

⚠️ If you did any changes in this phase make sure to repeat steps 4,5 and 6.

7. Create a pull request:
   1. Open the repository on github website
   2. Go to `Pull requests`
   3. Click on `New pull request`
   4. Chose your branch
   5. Click on `Create pull request`

8. Contact an admin to merge your pull request with the main branch.

## README.md Structure:

```md
# Chall_name 
<as will be displayed on CTFd>

## Description: 
<as will be displayed on CTFd>

## Author: 
<discord username>

## Brief: 
<Summary about your challenge>

## Flag: 
<FlagCTF{printable ASCII} or Dynamic>

```

## Dockerfile Templates

Rename the `template` folder and place your challenge files in `source` directory.

### [PWN](/pwn/template/)
### [Crypto](/crypto/template/)

### build.sh
Make sure to change `category_challenge_name` in all commands. Keep ports set to `1337` unless needed.
