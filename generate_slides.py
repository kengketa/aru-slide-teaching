import os
import re

def parse_plan(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    parts = []
    current_part = None
    current_day = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match Part
        part_match = re.match(r'Part (\d+): (.+)', line)
        if part_match:
            current_part = {
                'number': part_match.group(1),
                'title': part_match.group(2),
                'days': []
            }
            parts.append(current_part)
            continue

        # Match Day
        day_match = re.match(r'วันที่ (\d+): (.+)', line)
        if day_match:
            current_day = {
                'number': day_match.group(1),
                'title': day_match.group(2),
                'slides': []
            }
            if current_part:
                current_part['days'].append(current_day)
            continue

        # Match Slide
        slide_match = re.match(r'Slide (\d+): (.+)', line)
        if slide_match:
            slide_info = {
                'number': slide_match.group(1),
                'content': slide_match.group(2)
            }
            if current_day:
                current_day['slides'].append(slide_info)

    return parts

def generate_slides(parts):
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Prompt:wght@300;400;600&display=swap');

    :root {
        --primary: #FF8C00;
        --primary-light: #FFF4E5;
        --secondary: #2D3436;
        --white: #FFFFFF;
        --gray-light: #F9FAFB;
        --gray-medium: #E5E7EB;
        --text-dark: #1F2937;
        --text-muted: #6B7280;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: 'Inter', 'Prompt', sans-serif;
        margin: 0;
        padding: 0;
        background-color: var(--gray-light);
        color: var(--text-dark);
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        line-height: 1.6;
    }

    header {
        background-color: var(--white);
        padding: 2rem 1rem;
        text-align: center;
        border-bottom: 1px solid var(--gray-medium);
        position: relative;
    }

    header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), #FFB142);
    }

    .header-content {
        max-width: 1000px;
        margin: 0 auto;
    }

    .part-title {
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        color: var(--primary);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }

    .day-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--secondary);
    }

    main {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .slide-container {
        max-width: 960px;
        width: 100%;
        background-color: var(--white);
        padding: 4rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .slide-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 8px;
        background-color: var(--primary);
    }

    .slide-number {
        font-size: 1rem;
        color: var(--text-muted);
        font-weight: 600;
        margin-bottom: 2rem;
        display: inline-block;
        padding: 0.25rem 1rem;
        background-color: var(--primary-light);
        color: var(--primary);
        border-radius: 9999px;
    }

    h1 {
        font-size: 3rem;
        margin-bottom: 2rem;
        color: var(--text-dark);
        font-weight: 700;
        line-height: 1.2;
    }

    .nav-buttons {
        padding: 2rem;
        text-align: center;
        background-color: var(--white);
        border-top: 1px solid var(--gray-medium);
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    .btn {
        background-color: var(--white);
        color: var(--text-dark);
        border: 1px solid var(--gray-medium);
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        cursor: pointer;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.875rem;
        transition: var(--transition);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn:hover {
        border-color: var(--primary);
        color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.15);
    }

    .btn-primary {
        background-color: var(--primary);
        color: var(--white);
        border-color: var(--primary);
    }

    .btn-primary:hover {
        background-color: #E67E00;
        color: var(--white);
    }

    .btn.disabled {
        opacity: 0.3;
        cursor: not-allowed;
        pointer-events: none;
    }

    footer {
        padding: 1.5rem;
        text-align: center;
        font-size: 0.875rem;
        color: var(--text-muted);
        border-top: 1px solid var(--gray-medium);
        background-color: var(--gray-light);
    }

    .index-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .day-card {
        background: var(--white);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-top: 5px solid var(--primary);
        transition: var(--transition);
    }

    .day-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .day-card h3 {
        margin-top: 0;
        color: var(--secondary);
        font-size: 1.25rem;
        border-bottom: 1px solid var(--gray-medium);
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
    }

    .slide-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .slide-list li {
        margin-bottom: 0.5rem;
    }

    .slide-list a {
        color: var(--text-dark);
        text-decoration: none;
        font-size: 0.9rem;
        display: block;
        padding: 0.5rem;
        border-radius: 6px;
        transition: var(--transition);
    }

    .slide-list a:hover {
        background-color: var(--primary-light);
        color: var(--primary);
        padding-left: 0.75rem;
    }

    .part-section {
        grid-column: 1 / -1;
        margin-top: 2rem;
    }

    .part-badge {
        background: var(--primary);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 9999px;
        display: inline-block;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .info-container {
        display: flex;
        align-items: center;
        gap: 3rem;
        text-align: left;
        margin-top: 3rem;
        padding: 2rem;
        background: var(--gray-light);
        border-radius: 15px;
        border-left: 5px solid var(--primary);
    }

    .info-text {
        flex: 1;
        font-size: 1.25rem;
        color: var(--text-dark);
    }

    .info-icon {
        width: 120px;
        height: 120px;
        color: var(--primary);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .command-container {
        margin-top: 2rem;
        text-align: left;
        background: #282c34;
        border-radius: 10px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .command-header {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #abb2bf;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .command-header::before {
        content: '';
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #ff5f56;
        border-radius: 50%;
        box-shadow: 15px 0 0 #ffbd2e, 30px 0 0 #27c93f;
        margin-right: 35px;
    }

    .command-text {
        font-family: 'Courier New', Courier, monospace;
        color: #61afef;
        font-size: 1.1rem;
        margin: 0;
        white-space: pre-wrap;
    }

    .command-comment {
        color: #7f848e;
        font-style: italic;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        header {
            padding: 1.5rem 1rem;
        }

        .day-title {
            font-size: 1.1rem;
        }

        main {
            padding: 1rem;
        }

        .slide-container {
            padding: 2rem 1.5rem;
            border-radius: 12px;
        }

        h1 {
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }

        .info-container {
            flex-direction: column-reverse;
            gap: 1.5rem;
            padding: 1.5rem;
            text-align: center;
        }

        .info-text {
            font-size: 1rem;
        }

        .info-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto;
        }

        .command-container {
            padding: 1rem;
        }

        .command-text {
            font-size: 0.9rem;
        }

        .nav-buttons {
            padding: 1rem;
            flex-wrap: wrap;
        }

        .btn {
            padding: 0.6rem 1rem;
            font-size: 0.8rem;
            flex: 1;
            justify-content: center;
        }

        .index-grid {
            grid-template-columns: 1fr;
            padding: 1rem;
            gap: 1rem;
        }
    }
    """

    all_slides = []

    # Detailed info and icons mapping for all 60 slides
    # Each key is "day_slide" (e.g., "1_1" for Day 1 Slide 1)
    slide_details = {
        # Day 1: Mastering Git & Docker Essentials
        "1_1": {"info": "Version Control System (VCS) helps track code changes. Centralized (CVCS) uses one server, while Distributed (DVCS) like Git allows every user to have a full copy of the history.", "icon": "git-branch", "command": "# Install Git\n# macOS: brew install git\n# Windows: winget install --id Git.Git -e\n# Linux: sudo apt-get install git\n\n# Check Git version\ngit --version\n\n# Get help for a command\ngit help <command>\n\n# Configure global identity\ngit config --global user.name \"Name\"\ngit config --global user.email \"email@example.com\"\n\n# Check global configuration\ngit config --global --list\n\n# Set default editor (VS Code)\ngit config --global core.editor \"code --wait\"\n\n# Enable colored output\ngit config --global color.ui auto\n\n# List all aliases\ngit config --get-regexp alias\n\n# Clear global config\n# git config --global --unset user.name"},
        "1_2": {"info": "Set your identity with git config. Create SSH keys to securely connect and push code to remote repositories like GitHub without typing passwords every time. Install SourceTree (GUI) for a more visual Git experience.", "icon": "settings", "command": "# List all configurations\ngit config --list\n\n# Generate SSH Key\nssh-keygen -t ed25519 -C \"email@example.com\"\n\n# Start SSH agent\neval \"$(ssh-agent -s)\"\n\n# Add SSH key to agent\nssh-add ~/.ssh/id_ed25519\n\n# Copy SSH public key to clipboard (macOS)\npbcopy < ~/.ssh/id_ed25519.pub\n\n# Test SSH connection to GitHub\nssh -T git@github.com\n\n# Install SourceTree via winget (Windows)\nwinget install Atlassian.SourceTree\n\n# Check SSH key existence\nls -al ~/.ssh\n\n# Remove SSH key\n# rm ~/.ssh/id_ed25519\n\n# Create SSH config file\ntouch ~/.ssh/config"},
        "1_3": {"info": "Understand the Git workflow: Modified (changed files), Staged (prepared for commit), and Committed (safely stored in the database). Master essential commands like commit, stash, push, and pull to manage your code history and collaborate.", "icon": "refresh-cw", "command": "# Initialize repository\ngit init\n\n# Show status of files\ngit status\n\n# Stage all changes\ngit add .\n\n# Commit with message\ngit commit -m \"initial commit\"\n\n# List commit history\ngit log --oneline\n\n# View file changes\ngit diff\n\n# Unstage all changes\ngit reset\n\n# Remove a file from tracking\ngit rm --cached <file>\n\n# Show help for log\ngit log --help\n\n# Create a new file\ntouch readme.md"},
        "1_4": {"info": "Write clear, descriptive commit messages. Use git add to stage changes and git commit to save a snapshot of your project's current state.", "icon": "check-circle", "command": "# Stage specific file\ngit add filename.php\n\n# Commit with message\ngit commit -m \"feat: add login validation\"\n\n# Amend last commit\ngit commit --amend\n\n# Unstage a file\ngit reset HEAD filename.php\n\n# View changes in staged files\ngit diff --staged\n\n# Commit all tracked changes\ngit commit -am \"fix: typo in header\"\n\n# Revert a commit (creates new commit)\ngit revert <commit_hash>\n\n# Show commit details\ngit show <commit_hash>\n\n# List commit history (graph)\ngit log --graph --oneline --all\n\n# Reset to previous commit (caution!)\n# git reset --hard <commit_hash>"},
        "1_5": {"info": "The .gitignore file tells Git which files or folders to ignore. Common examples include vendor/, .env, node_modules/, and temporary log files.", "icon": "eye-off", "command": "# Create .gitignore file\ntouch .gitignore\n\n# Add vendor folder to ignore\necho \"vendor/\" >> .gitignore\n\n# List ignored files\ngit clean -ndX\n\n# Check why a file is ignored\ngit check-ignore -v filename.log\n\n# Force add an ignored file\ngit add -f secret.env\n\n# List all tracked files\ngit ls-files\n\n# Remove files that should be ignored\ngit rm -r --cached .\n\n# Ignore all .log files\necho \"*.log\" >> .gitignore\n\n# Global gitignore file\ngit config --global core.excludesfile ~/.gitignore_global\n\n# View .gitignore content\ncat .gitignore"},
        "1_6": {"info": "Collaborate with others by cloning repositories, pulling the latest changes from the server, and pushing your local commits to the remote branch.", "icon": "users", "command": "# Clone a repository\ngit clone https://github.com/user/repo.git\n\n# Add remote repository\ngit remote add origin https://github.com/user/repo.git\n\n# Push to main branch\ngit push -u origin main\n\n# Pull latest changes\ngit pull origin main\n\n# List remote repositories\ngit remote -v\n\n# Remove a remote\ngit remote remove origin\n\n# Change remote URL\ngit remote set-url origin <new_url>\n\n# Fetch from remote (no merge)\ngit fetch origin\n\n# Check remote branch info\ngit remote show origin\n\n# Create local branch from remote\ngit checkout -b dev origin/dev"},
        "1_7": {"info": "Docker containers are lightweight, portable, and isolate applications from the host OS. To get started, download and install Docker Desktop for your operating system from the official website.", "icon": "box", "command": "# Check Docker version\ndocker --version\n\n# Check Docker system info\ndocker info\n\n# Test Docker installation\ndocker run hello-world\n\n# Login to Docker Hub\ndocker login\n\n# List Docker contexts\ndocker context ls\n\n# Logout from Docker Hub\ndocker logout\n\n# Show Docker disk usage\ndocker system df\n\n# Prune unused Docker objects\ndocker system prune\n\n# List all running/stopped containers\ndocker ps -a\n\n# Search for image on Docker Hub\ndocker search nginx"},
        "1_8": {"info": "Images are read-only blueprints. Containers are live instances of images. Volumes allow you to persist data even if the container is deleted.", "icon": "layers", "command": "# List images\ndocker images\n\n# Remove an image\ndocker rmi <image_id>\n\n# Create a volume\ndocker volume create my-data\n\n# List volumes\ndocker volume ls\n\n# Inspect an image\ndocker inspect <image_id>\n\n# Pull an image\ndocker pull alpine\n\n# Tag an image\ndocker tag image:old image:new\n\n# Remove unused images\ndocker image prune\n\n# History of an image\ndocker history <image_name>\n\n# Remove a volume\ndocker volume rm my-data"},
        "1_9": {"info": "Master essential commands: docker run (start), docker ps (list), docker exec (run command inside), and docker stop (shut down).", "icon": "terminal", "command": "# Run nginx in background\ndocker run -d -p 8080:80 --name web nginx\n\n# List running containers\ndocker ps\n\n# Access container shell\ndocker exec -it web bash\n\n# Stop a container\ndocker stop web\n\n# Remove a container\ndocker rm -f web\n\n# View container logs\ndocker logs web\n\n# Restart a container\ndocker restart web\n\n# Pause a container\ndocker pause web\n\n# Copy file from host to container\ndocker cp local_file.txt web:/var/www/html/\n\n# List container processes\ndocker top web"},
        "1_10": {"info": "Docker Compose uses a YAML file to define and run multi-container applications, like a PHP app connected to a MySQL database.", "icon": "cpu", "command": "# Start services in background\ndocker-compose up -d\n\n# View service status\ndocker-compose ps\n\n# Stop and remove containers\ndocker-compose down\n\n# View logs\ndocker-compose logs -f\n\n# Build or rebuild services\ndocker-compose build\n\n# List running images\ndocker-compose images\n\n# Run command in service\ndocker-compose exec app php artisan list\n\n# Restart services\ndocker-compose restart\n\n# Stop services without removing\ndocker-compose stop\n\n# Start services without rebuilding\ndocker-compose start"},

        # Day 2: Laravel Sail & Development Environment
        "2_1": {"info": "Laravel Sail is a light CLI for interacting with Laravel's default Docker development environment. No need to install PHP or MySQL locally.", "icon": "anchor", "command": "# Install Sail into existing project\ncomposer require laravel/sail --dev\n\n# Publish Sail docker-compose file\nphp artisan sail:install\n\n# Start Sail\n./vendor/bin/sail up\n\n# Stop Sail\n./vendor/bin/sail stop\n\n# Check Sail version\n./vendor/bin/sail --version\n\n# Start Sail in background\n./vendor/bin/sail up -d\n\n# Check Sail status\n./vendor/bin/sail ps\n\n# View Sail logs\n./vendor/bin/sail logs\n\n# Rebuild Sail services\n./vendor/bin/sail build\n\n# Access Sail shell\n./vendor/bin/sail shell"},
        "2_2": {"info": "Install Laravel with Sail using a simple curl command. It sets up everything including PHP, MySQL, Redis, and more in minutes.", "icon": "download", "command": "# Install new Laravel app with Sail\ncurl -s \"https://laravel.build/my-app\" | bash\n\n# Specify services to install\ncurl -s \"https://laravel.build/my-app?with=mysql,redis\" | bash\n\n# Change directory to app\ncd my-app\n\n# Initial Sail startup\n./vendor/bin/sail up -d\n\n# Open app in browser\nopen http://localhost\n\n# Open PHPMyAdmin (if installed)\nopen http://localhost:8080\n\n# Stop all services\n./vendor/bin/sail down\n\n# Restart services\n./vendor/bin/sail restart\n\n# View version details\n./vendor/bin/sail artisan --version\n\n# Check node version in Sail\n./vendor/bin/sail node -v"},
        "2_3": {"info": "The docker-compose.yml file in a Sail project defines services like 'laravel.test', 'mysql', and 'selenium' for automated testing.", "icon": "file-text", "command": "# View docker-compose configuration\ncat docker-compose.yml\n\n# List running Sail containers\n./vendor/bin/sail ps\n\n# Check logs of specific service\n./vendor/bin/sail logs mysql\n\n# Rebuild Sail images\n./vendor/bin/sail build --no-cache\n\n# View docker-compose version\ndocker-compose --version\n\n# View service ports\ndocker-compose port mysql 3306\n\n# Stop a specific service\n./vendor/bin/sail stop mysql\n\n# Start a specific service\n./vendor/bin/sail up -d mysql\n\n# Remove all containers and volumes\n./vendor/bin/sail down -v\n\n# Validate docker-compose file\ndocker-compose config"},
        "2_4": {"info": "Use './vendor/bin/sail' to run commands. Creating a shell alias like 'alias sail=\"./vendor/bin/sail\"' makes it even faster to type.", "icon": "zap", "command": "# Set shell alias for Sail\nalias sail='./vendor/bin/sail'\n\n# Use alias to start Sail\nsail up -d\n\n# Run artisan via alias\nsail artisan list\n\n# Run composer via alias\nsail composer install\n\n# Stop all Sail services\nsail down\n\n# Permanent alias (macOS/Zsh)\necho \"alias sail='./vendor/bin/sail'\" >> ~/.zshrc\n\n# Permanent alias (Ubuntu/Bash)\necho \"alias sail='./vendor/bin/sail'\" >> ~/.bashrc\n\n# Reload shell config\nsource ~/.zshrc\n\n# Check if alias exists\nalias sail\n\n# Remove an alias\nunalias sail"},
        "2_5": {"info": "The .env file stores sensitive configuration. Sail automatically configures these values to connect services within the Docker network.", "icon": "lock", "command": "# Copy .env.example to .env\ncp .env.example .env\n\n# Generate application key\nsail artisan key:generate\n\n# Set DB_CONNECTION to mysql\n# DB_HOST=mysql\n\n# Check environment variables in Sail\nsail shell -c \"env\"\n\n# Restart Sail to apply .env changes\nsail restart\n\n# View current .env content\ncat .env\n\n# Clear config cache\nsail artisan config:clear\n\n# Cache config for performance\nsail artisan config:cache\n\n# List all Artisan configurations\nsail artisan config:show\n\n# Edit .env file (inside terminal)\nnano .env"},
        "2_6": {"info": "Easily add Redis for fast caching and Mailpit for a local email testing server by modifying your Sail configuration.", "icon": "plus-square", "command": "# Add new services to Sail\nsail artisan sail:add\n\n# Start specific service\nsail up redis mailpit\n\n# Access Mailpit web UI\nopen http://localhost:8025\n\n# Test Redis connection\nsail redis-cli ping\n\n# Flush Redis cache\nsail redis-cli flushall\n\n# List all Redis keys\nsail redis-cli keys \"*\"\n\n# Monitor Redis in real-time\nsail redis-cli monitor\n\n# Check Redis info\nsail redis-cli info\n\n# Stop Redis service\nsail stop redis\n\n# View Redis logs\nsail logs redis"},
        "2_7": {"icon": "database", "info": "Connect your favorite database tools like TablePlus or DBeaver to your Sail MySQL instance using the ports defined in .env.", "icon": "database", "command": "# Access MySQL shell via Sail\nsail mysql\n\n# List databases in MySQL\nsail mysql -e \"SHOW DATABASES;\"\n\n# Run MySQL client from host\nmysql -h 127.0.0.1 -P 3306 -u sail -p\n\n# Export database dump\nsail mysqldump db_name > dump.sql\n\n# Import database dump\nsail mysql db_name < dump.sql\n\n# Create new database\nsail mysql -e \"CREATE DATABASE new_db;\"\n\n# Show table structure\nsail mysql -e \"DESCRIBE table_name;\"\n\n# Run SQL file\nsail mysql db_name < schema.sql\n\n# Show MySQL process list\nsail mysql -e \"SHOW PROCESSLIST;\"\n\n# Repair MySQL tables\nsail mysqlcheck -u sail -p --repair db_name"},
        "2_8": {"icon": "package", "info": "Run PHP Artisan commands and NPM scripts directly through Sail, ensuring they run in the exact same environment as your app.", "command": "# Run artisan migrate\nsail artisan migrate\n\n# Install npm dependencies\nsail npm install\n\n# Run Vite development server\nsail npm run dev\n\n# Build production assets\nsail npm run build\n\n# Run PHP tests\nsail test\n\n# Run composer update\nsail composer update\n\n# Install specific PHP package\nsail composer require package/name\n\n# Run Laravel Pint (formatting)\nsail pint\n\n# Run PHPStan (static analysis)\nsail artisan analyze\n\n# Check PHP version\nsail php -v"},
        "2_9": {"icon": "bug", "info": "Learn how to use dd() (Dump and Die) for quick debugging in Laravel. It's a powerful tool to dump variables and stop execution to inspect data at any point in your code.", "command": "# Dump a single variable\ndd($user);\n\n# Dump multiple variables\ndd($user, $request->all(), $settings);\n\n# Use in Blade templates\n# @dd($variable)\n\n# Use within Artisan Tinker\nsail artisan tinker\n>>> dd(User::first());\n\n# Monitor Laravel logs\nsail shell -c \"tail -f storage/logs/laravel.log\"\n\n# Dump and continue (don't stop)\ndump($user);\n\n# Log message to file\nLog::info('debug message');\n\n# Print backtrace and die\ndd(debug_backtrace());\n\n# Dump variables to browser console\n# (Using Spatie Ray or Clockwork)\n\n# Clear log files\nsail shell -c \"truncate -s 0 storage/logs/laravel.log\""},
        "2_10": {"icon": "code", "info": "Build a basic CRUD (Create, Read, Update, Delete) application to verify that your environment, database, and routing are all working perfectly.", "command": "# Create model, migration, controller\nsail artisan make:model Post -mc\n\n# List all routes\nsail artisan route:list\n\n# Clear application cache\nsail artisan cache:clear\n\n# Clear route cache\nsail artisan route:clear\n\n# Clear view cache\nsail artisan view:clear\n\n# Create migration only\nsail artisan make:migration create_posts_table\n\n# Create resource controller\nsail artisan make:controller PostController --resource\n\n# Create factory for model\nsail artisan make:factory PostFactory\n\n# Run Laravel Tinker\nsail artisan tinker\n\n# Show app status\nsail artisan about"},

        # Day 3: Advanced DB & Team Workflow
        "3_1": {"icon": "database", "info": "Migrations are like version control for your database. They allow team members to share and modify the DB schema consistently using PHP code.", "command": "# Create new migration\nsail artisan make:migration create_posts_table\n\n# Run all pending migrations\nsail artisan migrate\n\n# Rollback last migration\nsail artisan migrate:rollback\n\n# Check migration status\nsail artisan migrate:status\n\n# View migration SQL without running\nsail artisan migrate --pretend\n\n# Rollback and re-run all migrations\nsail artisan migrate:refresh\n\n# Re-run all migrations and seed\nsail artisan migrate:fresh --seed\n\n# Reset and re-run all migrations\nsail artisan migrate:reset\n\n# Run migrations for specific connection\nsail artisan migrate --database=mysql_testing\n\n# Create migration for specific table\nsail artisan make:migration add_votes_to_users --table=users"},
        "3_2": {"icon": "layout", "info": "Define table structures, columns, and data types (string, integer, boolean) using the Schema builder in Laravel migration files.", "command": "# Create migration with table name\nsail artisan make:migration add_category_id_to_posts --table=posts\n\n# Refresh database and run seeds\nsail artisan migrate:fresh --seed\n\n# Wipe database (all tables)\nsail artisan db:wipe\n\n# Reset migrations\nsail artisan migrate:reset\n\n# Create migration for pivot table\nsail artisan make:migration create_post_tag_table\n\n# Rollback specific number of steps\nsail artisan migrate:rollback --step=2\n\n# Refresh specific number of steps\nsail artisan migrate:refresh --step=1\n\n# Show migration status as JSON\nsail artisan migrate:status --json\n\n# Install migration repository table\nsail artisan migrate:install\n\n# Create migration to rename table\nsail artisan make:migration rename_posts_to_articles"},
        "3_3": {"icon": "copy", "info": "Seeders populate your database with test data. Factories allow you to generate thousands of realistic records using the Faker library.", "command": "# Create a new seeder\nsail artisan make:seeder PostSeeder\n\n# Run specific seeder\nsail artisan db:seed --class=PostSeeder\n\n# Create a new factory\nsail artisan make:factory PostFactory\n\n# Run all seeders\nsail artisan db:seed\n\n# Test factory in Tinker\nsail artisan tinker --execute=\"Post::factory()->count(5)->make()\"\n\n# Create model and factory\nsail artisan make:model Category -f\n\n# Create factory with states\nsail artisan make:factory UserFactory --model=User\n\n# Run seeder in production (force)\nsail artisan db:seed --force\n\n# Run seeder for specific connection\nsail artisan db:seed --database=mysql\n\n# Generate hidden factory attributes\n# (Inside factory) 'password' => static::$password ??= Hash::make('password')"},
        "3_4": {"icon": "refresh-ccw", "info": "Use 'migrate:refresh' to roll back and re-run all migrations. This is useful for testing a clean state during development.", "command": "# Refresh and seed\nsail artisan migrate:refresh --seed\n\n# Refresh specific number of steps\nsail artisan migrate:refresh --step=3\n\n# Force run in production\nsail artisan migrate --force\n\n# Rollback all migrations and re-run\nsail artisan migrate:fresh\n\n# Check for uncommitted migrations\nsail artisan migrate:status\n\n# Squash migrations into single SQL file\nsail artisan schema:dump\n\n# Prune old migration files after squash\nsail artisan schema:dump --prune\n\n# Seed after fresh\nsail artisan migrate:fresh --seed\n\n# Reset specific steps\nsail artisan migrate:reset --step=1\n\n# Run migrations without output\nsail artisan migrate -q"},
        "3_5": {"icon": "git-branch", "info": "Follow a branching strategy: 'main' for production, 'develop' for integration, and 'feature/' branches for individual tasks.", "command": "# List all branches\ngit branch -a\n\n# Create and switch to new branch\ngit checkout -b feature/login-page\n\n# Switch back to main\ngit checkout main\n\n# Merge feature branch\ngit merge feature/login-page\n\n# Delete local branch\ngit branch -d feature/login-page\n\n# Rename current branch\ngit branch -m new-name\n\n# Delete remote branch\ngit push origin --delete feature/login-page\n\n# List merged branches\ngit branch --merged\n\n# List branches not merged yet\ngit branch --no-merged\n\n# View branches with last commit info\ngit branch -v"},
        "3_6": {"icon": "git-pull-request", "info": "Pull Requests (PRs) facilitate code review. Team members check each other's code for quality and bugs before merging into the main branch.", "command": "# Push local branch to remote\ngit push -u origin feature/login-page\n\n# List remote branches\ngit branch -r\n\n# Fetch updates from remote\ngit fetch origin\n\n# Compare branches\ngit diff main..feature/login-page\n\n# Pull updates into current branch\ngit pull origin main\n\n# Create pull request via GitHub CLI\ngh pr create --title \"Add login\"\n\n# List open pull requests\ngh pr list\n\n# Checkout a pull request locally\ngh pr checkout 123\n\n# View pull request status\ngh pr status\n\n# Merge pull request\ngh pr merge"},
        "3_7": {"icon": "alert-triangle", "info": "Merge conflicts happen when two people edit the same line. Learn to use diff tools to resolve these conflicts manually and safely.", "command": "# Rebase current branch on main\ngit rebase main\n\n# Abort merge in case of conflict\ngit merge --abort\n\n# Continue rebase after fixing conflict\ngit rebase --continue\n\n# View file with conflict markers\ncat conflicting_file.php\n\n# Mark file as resolved\ngit add resolved_file.php\n\n# Abort rebase\ngit rebase --abort\n\n# Skip a commit during rebase\ngit rebase --skip\n\n# Use mergetool (if configured)\ngit mergetool\n\n# Show common ancestor\ngit merge-base branchA branchB\n\n# Checkout version from 'ours' during conflict\ngit checkout --ours filename.php"},
        "3_8": {"icon": "users", "info": "Work in teams to build features. Use Git to sync your progress and resolve integration issues in a simulated real-world environment.", "command": "# Stash changes before pull\ngit stash\n\n# Pop stashed changes\ngit stash pop\n\n# Apply stash without removing\ngit stash apply\n\n# Show stash list\ngit stash list\n\n# Clear all stashes\ngit stash clear\n\n# Stash with a message\ngit stash save \"working on auth\"\n\n# Stash specific file\ngit stash push path/to/file.php\n\n# Create branch from stash\ngit stash branch new-branch-name\n\n# View stash diff\ngit stash show -p\n\n# Drop specific stash\ngit stash drop stash@{0}"},
        "3_9": {"icon": "lock", "info": "The lock files (composer.lock, package-lock.json) ensure everyone on the team installs the exact same versions of all dependencies.", "command": "# Install exactly from lock file\nsail composer install\n\n# Update dependencies and lock file\nsail composer update\n\n# Install npm dependencies from lock\nsail npm ci\n\n# Check for security vulnerabilities\nsail composer audit\n\n# List installed packages\nsail composer show\n\n# Update specific package\nsail composer update vendor/package\n\n# Check why a package is installed\nsail composer why vendor/package\n\n# List packages with licenses\nsail composer license\n\n# Validate composer.json\nsail composer validate\n\n# Clear composer cache\nsail composer clear-cache"},
        "3_10": {"icon": "clock", "info": "Offload heavy tasks like sending emails or processing images to background jobs using Laravel's Queue system and Docker workers.", "command": "# Create new job class\nsail artisan make:job SendWelcomeEmail\n\n# Start queue worker\nsail artisan queue:work\n\n# Monitor failed jobs\nsail artisan queue:failed\n\n# Retry failed jobs\nsail artisan queue:retry all\n\n# Clear all failed jobs\nsail artisan queue:flush\n\n# Restart queue worker\nsail artisan queue:restart\n\n# List all failed jobs\nsail artisan queue:list\n\n# Run specific queue\nsail artisan queue:work --queue=high,default\n\n# Run job once\nsail artisan queue:work --once\n\n# Work on failed jobs individually\nsail artisan queue:retry <id>"},

        # Day 4: Frontend Development with Vue 3
        "4_1": {"icon": "monitor", "info": "Modern CMS use Headless (API-only) or Hybrid approaches. Vue 3 provides a reactive and component-based way to build these dynamic interfaces.", "command": "# Install Vue 3 into existing project\nnpm install vue@latest\n\n# Create Vue project (standalone)\nnpm create vue@latest\n\n# Install Vue Router\nnpm install vue-router@4\n\n# Install Axios for API calls\nnpm install axios\n\n# Check Vue version\nnpm list vue\n\n# Initialize Vue app\n# createApp(App).mount('#app')\n\n# Install Pinia (State Management)\nnpm install pinia\n\n# Install Vite Vue plugin\nnpm install @vitejs/plugin-vue --save-dev\n\n# Create Vue component template\ntouch resources/js/components/Example.vue\n\n# Run dev server\nnpm run dev"},
        "4_2": {"icon": "figma", "info": "Before coding, analyze UI mockups. Identify reusable parts and plan the component hierarchy for a maintainable frontend architecture.", "command": "# Create directory for components\nmkdir -p resources/js/components/ui\n\n# Create directory for views/pages\nmkdir -p resources/js/views\n\n# Create layout directory\nmkdir -p resources/js/layouts\n\n# Initialize git in frontend\ngit add resources/js\n\n# List component files\nfind resources/js/components -name \"*.vue\"\n\n# Create BaseButton component\ntouch resources/js/components/ui/BaseButton.vue\n\n# Create BaseInput component\ntouch resources/js/components/ui/BaseInput.vue\n\n# Create Dashboard view\ntouch resources/js/views/Dashboard.vue\n\n# Create Auth layout\ntouch resources/js/layouts/AuthLayout.vue\n\n# Create App layout\ntouch resources/js/layouts/AppLayout.vue"},
        "4_3": {"icon": "star", "info": "Set up Vue 3 within Laravel using Vite. We'll use the Composition API or Options API to manage component logic and state.", "command": "# Install Vite Vue plugin\nsail npm install @vitejs/plugin-vue --dev\n\n# Run Vite development server\nsail npm run dev\n\n# Build assets for production\nsail npm run build\n\n# Check Vite version\nsail npm exec vite --version\n\n# Preview production build\nsail npm run preview\n\n# Clear Vite cache\nsail npm exec vite --force\n\n# List all npm scripts\nsail npm run\n\n# Update all npm packages\nsail npm update\n\n# Check for outdated packages\nsail npm outdated\n\n# Install Vite dev server types\nsail npm install @types/vite --dev"},
        "4_4": {"icon": "wind", "info": "Tailwind CSS allows for rapid styling using utility classes. Integrate it to create custom, responsive designs without leaving your HTML.", "command": "# Install Tailwind CSS and tools\nsail npm install -D tailwindcss postcss autoprefixer\n\n# Initialize Tailwind config\nnpx tailwindcss init -p\n\n# Run Tailwind CLI watcher\nnpx tailwindcss -i ./src/input.css -o ./dist/output.css --watch\n\n# Minify CSS for production\nnpx tailwindcss -o ./dist/output.css --minify\n\n# Check Tailwind version\nnpx tailwindcss --version\n\n# List all utility classes\n# (Refer to documentation or VS Code extension)\n\n# Remove unused CSS (Purge)\n# (Automatically handled by Tailwind v3)\n\n# Generate custom config file\nnpx tailwindcss init tailwind.config.js --full\n\n# Check for CSS errors\nnpx postcss resources/css/app.css"},
        "4_5": {"icon": "component", "info": "Build a library of reusable UI components like buttons, inputs, and cards. This ensures visual consistency and speeds up development.", "command": "# Create a BaseButton component\ntouch resources/js/components/ui/BaseButton.vue\n\n# Create a BaseInput component\ntouch resources/js/components/ui/BaseInput.vue\n\n# Register components globally in app.js\n# app.component('BaseButton', BaseButton)\n\n# List all UI components\nls resources/js/components/ui\n\n# Run linter on components\nsail npm run lint\n\n# Create Card component\ntouch resources/js/components/ui/Card.vue\n\n# Create Modal component\ntouch resources/js/components/ui/Modal.vue\n\n# Create Alert component\ntouch resources/js/components/ui/Alert.vue\n\n# Create Badge component\ntouch resources/js/components/ui/Badge.vue\n\n# Create Loader component\ntouch resources/js/components/ui/Loader.vue"},
        "4_6": {"icon": "sidebar", "info": "Create a Master Layout with persistent elements like a sidebar and navbar, using Vue slots to inject page-specific content.", "command": "# Create AppLayout.vue\ntouch resources/js/layouts/AppLayout.vue\n\n# Create Navigation components\ntouch resources/js/components/Navbar.vue\ntouch resources/js/components/Sidebar.vue\n\n# Update main entry point app.js\nsed -i '' 's/old/new/g' resources/js/app.js\n\n# Verify layout structure\ncat resources/js/layouts/AppLayout.vue\n\n# Create AuthLayout.vue\ntouch resources/js/layouts/AuthLayout.vue\n\n# Create GuestLayout.vue\ntouch resources/js/layouts/GuestLayout.vue\n\n# Create Dashboard header\ntouch resources/js/components/DashboardHeader.vue\n\n# Create User menu component\ntouch resources/js/components/UserMenu.vue\n\n# Create Breadcrumbs component\ntouch resources/js/components/Breadcrumbs.vue"},
        "4_7": {"icon": "activity", "info": "Manage application state. Use props to pass data down and events to communicate up, or use Pinia for more complex global state.", "command": "# Install Pinia store\nnpm install pinia\n\n# Create a store file\ntouch resources/js/stores/user.js\n\n# Debug state with Vue Devtools\n# Open browser devtools > Vue tab\n\n# Test store logic in Vitest\nsail npm run test:unit\n\n# Check Pinia version\nnpm list pinia\n\n# Initialize Pinia in main.js\n# app.use(createPinia())\n\n# Define a store (Composition style)\n# export const useUserStore = defineStore('user', () => { ... })\n\n# Use store in component\n# const store = useUserStore();\n\n# Reset store state\n# store.$reset();\n\n# Watch store changes\n# store.$subscribe((mutation, state) => { ... })"},
        "4_8": {"icon": "smartphone", "info": "Use Tailwind's responsive prefixes (sm:, md:, lg:) to ensure your CMS dashboard looks great on phones, tablets, and desktops.", "command": "# Use Tailwind grid for layout\n# <div class=\"grid grid-cols-1 md:grid-cols-2\"></div>\n\n# Use Tailwind hidden/block for responsive menu\n# <div class=\"hidden md:block\">Sidebar</div>\n\n# Custom screen size in tailwind.config.js\n# screens: { 'xs': '480px' }\n\n# Check responsive design in Chrome\n# CMD+SHIFT+M (Device Mode)\n\n# Analyze CSS bundle size\nsail npm run build -- --report\n\n# Set container max-width\n# <div class=\"container mx-auto px-4\"></div>\n\n# Use flexbox for responsive alignment\n# <div class=\"flex flex-col md:flex-row\"></div>\n\n# Add responsive padding/margin\n# <div class=\"p-4 md:p-8\"></div>\n\n# Responsive typography\n# <h1 class=\"text-xl md:text-3xl\">Title</h1>\n\n# Hide scrollbar on mobile\n# <div class=\"overflow-x-auto scrollbar-hide\"></div>"},
        "4_9": {"icon": "edit-3", "info": "Handle user input with v-model. Validate data on the frontend before sending it to the Laravel API for processing.", "command": "# Install Vuelidate for validation\nnpm install @vuelidate/core @vuelidate/validators\n\n# Use v-model in component\n# <input v-model=\"state.name\" />\n\n# Handle form submit event\n# <form @submit.prevent=\"onSubmit\">\n\n# Reset form data\n# Object.assign(state, initialState)\n\n# Watch data changes\n# watch(() => state.email, (newVal) => { ... })\n\n# Multi-binding v-model\n# <custom-input v-model:title=\"state.title\" />\n\n# Use reactive() for form state\n# const form = reactive({ name: '', email: '' });\n\n# Validate on blur\n# <input @blur=\"v$.name.$touch()\" />\n\n# Show validation errors\n# <span v-if=\"v$.name.$error\">Name is required</span>\n\n# Set form to loading state during submit\n# const isLoading = ref(false);"},
        "4_10": {"icon": "check-square", "info": "Put it all together: create your first interactive Dashboard page with real components and a responsive layout.", "command": "# Create Dashboard.vue view\ntouch resources/js/views/Dashboard.vue\n\n# Run development server\nsail npm run dev\n\n# Build for production\nsail npm run build\n\n# Check for errors in browser console\n# Inspect > Console\n\n# Deploy assets to CDN/Storage\nsail artisan storage:link\n\n# Check generated asset files\nls public/build/assets\n\n# Clean build directory\nrm -rf public/build\n\n# Run Vite build with manifest\nsail npm run build -- --manifest\n\n# View Vite stats\nsail npm run build -- --report\n\n# Lint your code\nsail npm run lint"},

        # Day 5: Backend API & Data Modeling
        "5_1": {"icon": "target", "info": "Transition from frontend to backend. Define the API endpoints needed to power the CMS features we've designed.", "command": "# Create API controller\nsail artisan make:controller Api/PostController --api\n\n# List only API routes\nsail artisan route:list --path=api\n\n# Create API route file\ntouch routes/api.php\n\n# Test API with curl\ncurl http://localhost/api/posts\n\n# Use Postman/Insomnia to test endpoints\n\n# Filter routes by name\nsail artisan route:list --name=posts\n\n# Check route middleware\nsail artisan route:list --columns=method,uri,name,middleware\n\n# Cache API routes\nsail artisan route:cache\n\n# Clear route cache\nsail artisan route:clear\n\n# Show specific route info\nsail artisan route:show api/posts"},
        "5_2": {"icon": "database", "info": "Design a robust schema for articles, categories, and media. Think about which fields are required and how they will be indexed.", "command": "# Create migration for posts table\nsail artisan make:migration create_posts_table\n\n# Add unique index to slug\n# $table->string('slug')->unique();\n\n# Refresh database and run migrations\nsail artisan migrate:fresh\n\n# View database schema info\nsail artisan model:show Post\n\n# List all database tables\nsail mysql -e \"SHOW TABLES;\"\n\n# Show column details\nsail mysql -e \"DESCRIBE posts;\"\n\n# Check table size\nsail mysql -e \"SELECT table_name, data_length FROM information_schema.tables WHERE table_schema = 'sail';\"\n\n# Create index migration\nsail artisan make:migration add_index_to_posts_title\n\n# Check database connection\nsail artisan db:show\n\n# List table indexes\nsail mysql -e \"SHOW INDEX FROM posts;\""},
        "5_3": {"icon": "link", "info": "Define Eloquent relationships: One-to-Many for categories and articles, and Many-to-Many for tagging systems.", "command": "# Test relationships in Tinker\nsail artisan tinker --execute=\"$cat = Category::first(); $cat->posts;\"\n\n# Create migration for pivot table\nsail artisan make:migration create_post_tag_table\n\n# Define BelongsTo relationship\n# return $this->belongsTo(Category::class);\n\n# Eager load relationships\n# Post::with('category')->get();\n\n# Check relationship existence\n# $post->category()->exists();\n\n# Count related records\n# Post::withCount('comments')->get();\n\n# Filter by relationship\n# Post::has('comments')->get();\n\n# Filter by relationship content\n# Post::whereHas('comments', function($q) { ... })->get();\n\n# Load missing relationships\n# $post->loadMissing('author');\n\n# Define Polymorphic relationship\n# return $this->morphMany(Comment::class, 'commentable');"},
        "5_4": {"icon": "trash-2", "info": "Use Soft Deletes to prevent accidental data loss. This allows you to 'trash' items and restore them later if needed.", "command": "# Add soft deletes to migration\n# $table->softDeletes();\n\n# Soft delete a record\n# $post->delete();\n\n# Restore a soft deleted record\n# $post->restore();\n\n# Force delete (permanent)\n# $post->forceDelete();\n\n# Query including trashed records\n# Post::withTrashed()->get();\n\n# Query ONLY trashed records\n# Post::onlyTrashed()->get();\n\n# Check if record is trashed\n# $post->trashed();\n\n# Restore all trashed records\n# Post::onlyTrashed()->restore();\n\n# Permanently delete all trashed\n# Post::onlyTrashed()->forceDelete();\n\n# Create migration for soft deletes\nsail artisan make:migration add_soft_deletes_to_posts --table=posts"},
        "5_5": {"icon": "fast-forward", "info": "Generate massive amounts of test data. This helps identify performance bottlenecks and pagination needs in your API.", "command": "# Generate 100 posts via factory\nsail artisan tinker --execute=\"Post::factory()->count(100)->create()\"\n\n# Run seeders\nsail artisan db:seed\n\n# Benchmarking API response\nab -n 100 -c 10 http://localhost/api/posts\n\n# Check pagination in response\n# GET /api/posts?page=2\n\n# Set default pagination limit in model\n# protected $perPage = 15;\n\n# Simple pagination (next/prev only)\n# Post::paginate(15)->simplePaginate(15);\n\n# Cursor pagination (for large datasets)\n# Post::cursorPaginate(15);\n\n# Customizing pagination view\nsail artisan vendor:publish --tag=laravel-pagination\n\n# Appending to pagination links\n# $posts->appends(['sort' => 'votes']);\n\n# Checking total records in Tinker\nsail artisan tinker --execute=\"Post::count();\""},
        "5_6": {"icon": "box", "info": "Configure Eloquent models with fillable attributes, casts, and hidden fields to ensure data integrity and security.", "command": "# List fillable attributes\n# protected $fillable = ['title', 'content'];\n\n# Set attribute casting\n# protected $casts = ['is_published' => 'boolean'];\n\n# Hide sensitive fields\n# protected $hidden = ['password', 'token'];\n\n# Set default attribute values\n# protected $attributes = ['status' => 'draft'];\n\n# Prevent mass assignment exception\n# protected $guarded = [];\n\n# Define custom date format\n# protected $dateFormat = 'U';\n\n# Disable timestamps\n# public $timestamps = false;\n\n# Set custom table name\n# protected $table = 'my_posts';\n\n# Set custom primary key\n# protected $primaryKey = 'post_id';\n\n# Disable auto-incrementing key\n# public $incrementing = false;"},
        "5_7": {"icon": "json", "info": "API Resources allow you to transform your models into the exact JSON format your frontend expects, decoupling your DB from your API.", "command": "# Create API Resource\nsail artisan make:resource PostResource\n\n# Create Resource Collection\nsail artisan make:resource PostCollection\n\n# Return resource in controller\n# return new PostResource($post);\n\n# Wrap response in 'data' key\n# JsonResource::withoutWrapping();\n\n# Add meta data to response\n# return $resource->additional(['meta' => 'data']);\n\n# Customize resource response headers\n# $resource->toResponse($request)->header('X-Value', 'True');\n\n# Use resource for collections\n# PostResource::collection(Post::all());\n\n# Create anonymous resource collection\n# PostResource::collection($posts);\n\n# Transform attributes in resource\n# 'created_at' => $this->created_at->format('Y-m-d')\n\n# Include nested resources\n# 'user' => new UserResource($this->user)"},
        "5_8": {"icon": "filter", "info": "Customize JSON responses: include related data, change field names, or hide sensitive information based on user roles.", "command": "# Conditional relationship loading\n# $this->whenLoaded('category')\n\n# Conditional attribute\n# $this->when($this->is_admin, 'secret-data')\n\n# Flatten resource\n# return parent::toArray($request);\n\n# Customize resource key\n# public static $wrap = 'post';\n\n# Test resource output in Tinker\nsail artisan tinker --execute=\"new PostResource(Post::first())\"\n\n# Add conditional metadata\n# $this->when($request->user()->isAdmin(), ['key' => 'val'])\n\n# Merge attributes conditionally\n# $this->mergeWhen($this->is_admin, ['role' => 'admin'])\n\n# Transform value into Resource\n# 'tags' => TagResource::collection($this->whenLoaded('tags'))\n\n# Accessing request in resource\n# $request->user()\n\n# Customizing root wrap\n# PostResource::wrap('articles');"},
        "5_9": {"icon": "shuffle", "info": "Keep controllers 'thin' by moving complex business logic into Service classes or Action classes for better testability.", "command": "# Create Service class\nmkdir -p app/Services && touch app/Services/PostService.php\n\n# Create Action class\nmkdir -p app/Actions && touch app/Actions/CreatePostAction.php\n\n# Inject service into controller\n# public function __construct(PostService $service)\n\n# Run unit tests for service\nsail artisan test --filter=PostServiceTest\n\n# List all services\nfind app/Services -name \"*.php\"\n\n# Create a trait\ntouch app/Traits/Slugger.php\n\n# Use trait in model\n# use Slugger;\n\n# Create a Repository class\ntouch app/Repositories/PostRepository.php\n\n# Bind interface to implementation\n# $this->app->bind(PostInterface::class, PostRepository::class);\n\n# Check service provider registration\nsail artisan about"},
        "5_10": {"icon": "shield", "info": "Secure your API. Use Laravel Sanctum or Passport for token-based authentication to protect routes from unauthorized access.", "command": "# Install Laravel Sanctum\nsail artisan sanctum:install\n\n# Protect routes with middleware\n# Route::middleware('auth:sanctum')\n\n# Create API token for user\n# $user->createToken('token-name')->plainTextToken;\n\n# Test authenticated request\ncurl -H \"Authorization: Bearer <token>\" http://localhost/api/user\n\n# Revoke user tokens\n# $user->tokens()->delete();\n\n# Check if token has ability\n# $user->tokenCan('post:create')\n\n# Authenticate SPA (Session-based)\n# Ensure SANCTUM_STATEFUL_DOMAINS is set\n\n# List user tokens in Tinker\nsail artisan tinker --execute=\"User::first()->tokens\"\n\n# Customizing token expiration\n# 'expiration' => 60\n\n# Refreshing tokens\n# (Client-side logic or new token generation)"},

        # Day 6: Integration & Final Deployment
        "6_1": {"icon": "link-2", "info": "Use Axios in Vue 3 to fetch data from your Laravel API. Handle loading states and errors gracefully for a better user experience.", "command": "# Install Axios\nnpm install axios\n\n# GET request with Axios\n# axios.get('/api/posts').then(res => ...)\n\n# Handle errors with catch\n# axios.get('/api/posts').catch(err => console.error(err))\n\n# Set base URL for Axios\n# axios.defaults.baseURL = 'http://localhost/api';\n\n# Intercept requests for auth\n# axios.interceptors.request.use(config => { ... })\n\n# Use async/await for requests\n# const res = await axios.get('/api/posts');\n\n# Cancel requests (AbortController)\n# const controller = new AbortController();\n\n# Global Axios configuration\n# axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';\n\n# Handle 401 Unauthorized globally\n# axios.interceptors.response.use(...)\n\n# Fetch with params\n# axios.get('/api/posts', { params: { page: 1 } })"},
        "6_2": {"icon": "save", "info": "Implement the full flow: user fills a form, Vue sends a POST request, Laravel validates and saves, and the UI updates.", "command": "# POST request with data\n# axios.post('/api/posts', formData)\n\n# Create Request class in Laravel\nsail artisan make:request StorePostRequest\n\n# Validate in controller\n# $request->validated();\n\n# Send response from Laravel\n# return response()->json($post, 201);\n\n# Refresh Vue component data after save\n\n# Handle validation errors in Vue\n# const errors = err.response.data.errors;\n\n# PUT/PATCH for updates\n# axios.patch(`/api/posts/${id}`, data)\n\n# DELETE a record\n# axios.delete(`/api/posts/${id}`)\n\n# Reset form after success\n# form.value = { ...initialValue };\n\n# Show success notification (Toast)\n# toast.success('Saved!');"},
        "6_3": {"icon": "image", "info": "Handle file uploads securely. Laravel's Storage facade makes it easy to save files locally or on cloud services like Amazon S3.", "command": "# Store uploaded file\n# $path = $request->file('avatar')->store('avatars');\n\n# Use specific disk\n# Storage::disk('s3')->put('file.txt', 'content');\n\n# Check if file exists\n# Storage::exists('file.jpg');\n\n# Get file URL\n# Storage::url('file.jpg');\n\n# Delete a file\n# Storage::delete('file.jpg');\n\n# Get temporary URL (S3)\n# Storage::temporaryUrl('file.jpg', now()->addMinutes(5));\n\n# Download a file\n# return Storage::download('file.pdf');\n\n# Get file metadata\n# Storage::size('file.jpg');\n\n# Copy file between disks\n# Storage::disk('local')->copy('f1.txt', 'f2.txt');\n\n# List all files in directory\n# Storage::files('photos');"},
        "6_4": {"icon": "grid", "info": "Build a Media Library UI where users can upload, browse, and select existing images for their content without re-uploading.", "command": "# Link public storage to web folder\nsail artisan storage:link\n\n# List all files in storage directory\nsail shell -c \"ls storage/app/public/uploads\"\n\n# Create Media controller\nsail artisan make:controller MediaController\n\n# Get all media via API\n# Media::all();\n\n# Use spatie/laravel-medialibrary package\n# sail composer require \"spatie/laravel-medialibrary:^11.0.0\"\n\n# Register media collection in model\n# public function registerMediaCollections(): void\n\n# Upload to library\n# $model->addMedia($file)->toMediaCollection('images');\n\n# Retrieve image URL\n# $model->getFirstMediaUrl('images', 'thumb');\n\n# Delete media from library\n# $media->delete();\n\n# Optimize images on upload\n# (Using Spatie's Image Optimizer)"},
        "6_5": {"icon": "server", "info": "Understand the difference between development (Sail) and production Docker setups. Focus on security, performance, and stability.", "command": "# Build production image\ndocker build -t my-app:prod .\n\n# Run container in production mode\ndocker run -e APP_ENV=production my-app:prod\n\n# Check container resource usage\ndocker stats\n\n# Prune unused docker objects\ndocker system prune -a\n\n# List container networks\ndocker network ls\n\n# Check Docker disk usage\ndocker system df\n\n# Inspect production container\ndocker inspect <id>\n\n# Export production logs\ndocker logs <id> > prod_logs.txt\n\n# Run security audit on Dockerfile\ndocker scan my-app:prod\n\n# List images by tag\ndocker images --filter \"reference=my-app:*\""},
        "6_6": {"icon": "zap", "info": "Optimize your production Dockerfile using multi-stage builds to create tiny, high-performance images ready for the cloud.", "command": "# Build multi-stage Dockerfile\ndocker build -t my-app:slim -f Dockerfile.prod .\n\n# Check image size\ndocker images my-app:slim\n\n# Scan image for vulnerabilities\ndocker scan my-app:slim\n\n# Export image to tar file\ndocker save my-app:slim > app.tar\n\n# Import image from tar file\ndocker load < app.tar\n\n# List image layers\ndocker history my-app:slim\n\n# Remove all untagged images\ndocker rmi $(docker images -f \"dangling=true\" -q)\n\n# Compare image sizes\ndocker images\n\n# Compress image with Docker Slim\n# docker-slim build my-app:prod\n\n# Use Alpine base image for smallest size\n# FROM php:8.3-fpm-alpine"},
        "6_7": {"icon": "settings", "info": "Configure Nginx to serve your application, handle SSL certificates for HTTPS, and manage static asset caching.", "command": "# Test Nginx configuration\nnginx -t\n\n# Reload Nginx without downtime\nservice nginx reload\n\n# Install Certbot for SSL (Let's Encrypt)\nsudo apt-get install certbot python3-certbot-nginx\n\n# Generate SSL certificate\nsudo certbot --nginx\n\n# Check Nginx access logs\ntail -f /var/log/nginx/access.log\n\n# Check Nginx error logs\ntail -f /var/log/nginx/error.log\n\n# Enable site in Nginx\nln -s /etc/nginx/sites-available/my-app /etc/nginx/sites-enabled/\n\n# Restart Nginx service\nsudo systemctl restart nginx\n\n# Check Nginx status\nsudo systemctl status nginx\n\n# View active Nginx connections\nnetstat -an | grep :80 | wc -l"},
        "6_8": {"icon": "cloud-lightning", "info": "Set up a deployment workflow. Automate updates using CI/CD tools or simple Git hooks to push code to your live server.", "command": "# Create Git hook for deployment\ntouch .git/hooks/post-receive\n\n# Pull latest on production server\ngit pull origin main\n\n# Run production migrations\nphp artisan migrate --force\n\n# Optimize Laravel for production\nphp artisan optimize\n\n# Restart queue workers\nphp artisan queue:restart\n\n# Cache views for production\nphp artisan view:cache\n\n# Cache routes for production\nphp artisan route:cache\n\n# Clear all caches (if needed)\nphp artisan cache:clear\n\n# Check Laravel version on production\nphp artisan --version\n\n# Maintenance mode (On)\nphp artisan down\n\n# Maintenance mode (Off)\nphp artisan up"},
        "6_9": {"icon": "heart", "info": "Monitor your live application. Use logs and health checks to ensure your containers are running smoothly and respond to issues quickly.", "command": "# View container logs (last 50 lines)\ndocker logs --tail 50 <container_id>\n\n# Check container health status\ndocker inspect --format='{{json .State.Health}}' <id>\n\n# Monitor CPU/Memory in real-time\ntop\n\n# Check disk space usage\ndf -h\n\n# Test app endpoint with curl\ncurl -I https://my-app.com\n\n# Monitor system logs\ntail -f /var/log/syslog\n\n# Check memory usage of PHP-FPM\nps aux | grep php-fpm\n\n# Monitor active database connections\nsail mysql -e \"SHOW PROCESSLIST;\"\n\n# Check Laravel log file size\ndu -sh storage/logs/laravel.log\n\n# Tail Laravel logs in real-time\ntail -f storage/logs/laravel.log"},
        "6_10": {"icon": "help-circle", "info": "Wrap up the course! Review key concepts, share resources for further learning, and answer final questions from the seminar.", "command": "# Final check of all services\ndocker-compose ps\n\n# Print success message\necho \"Seminar Complete!\"\n\n# Clean up temporary files\nrm -rf storage/framework/views/*\n\n# Export final presentation index\n# open index.html\n\n# Farewell command\nexit\n\n# Clear all Docker resources (caution!)\n# docker system prune -a --volumes\n\n# Check project version\ncat package.json | grep version\n\n# Show total commits in project\ngit rev-list --count HEAD\n\n# List all seminar files\nls -R slides/\n\n# Open seminar repository\nopen https://github.com/kengketa/aru-slide-teaching"},
    }

    all_slides = []
    for part in parts:
        for day in part['days']:
            for slide in day['slides']:
                all_slides.append({
                    'part_title': part['title'],
                    'day_title': day['title'],
                    'day_num': day['number'],
                    'slide_num': slide['number'],
                    'content': slide['content']
                })

    # Create output directory
    if not os.path.exists('slides'):
        os.makedirs('slides')

    # Generate index.html
    index_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seminar Slides - Index</title>
    <style>
        {css}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="part-title">Seminar 2026</div>
            <div class="day-title">Course Curriculum & Slides</div>
        </div>
    </header>
    <main style="display:block;">
        <div class="index-grid">
    """

    for part in parts:
        index_html += f"""
        <div class="part-section">
            <span class="part-badge">Part {part['number']}</span>
            <h2 style="margin-top: 0.5rem; color: var(--secondary);">{part['title']}</h2>
        </div>"""
        for day in part['days']:
            index_html += f"""
            <div class="day-card">
                <h3>วันที่ {day['number']}: {day['title']}</h3>
                <ul class="slide-list">"""
            for slide in day['slides']:
                filename = f"slide_{day['number']}_{slide['number']}.html"
                index_html += f'<li><a href="slides/{filename}">Slide {slide["number"]}: {slide["content"]}</a></li>'
            index_html += "</ul></div>"

    index_html += """
        </div>
    </main>
    <footer>วิทยากร: นายสัจพงศ์ พงศ์ธีรโชติกุล | &copy; 2026 Presentation System</footer>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    # Generate slide pages
    for i, s in enumerate(all_slides):
        filename = f"slide_{s['day_num']}_{s['slide_num']}.html"
        prev_link = f"slide_{all_slides[i-1]['day_num']}_{all_slides[i-1]['slide_num']}.html" if i > 0 else "#"
        next_link = f"slide_{all_slides[i+1]['day_num']}_{all_slides[i+1]['slide_num']}.html" if i < len(all_slides) - 1 else "#"

        prev_class = "disabled" if i == 0 else ""
        next_class = "disabled" if i == len(all_slides) - 1 else ""

        # Get extra details
        key = f"{s['day_num']}_{s['slide_num']}"
        details = slide_details.get(key, {"info": "Additional information for this topic will be provided during the seminar.", "icon": "info", "command": "# No commands for this slide"})

        icon_name = details.get('icon', 'info')
        command_html = ""
        if 'command' in details:
            cmd = details['command']
            # Basic highlighting for comments
            highlighted_cmd = []
            for line in cmd.split('\n'):
                if line.startswith('#'):
                    highlighted_cmd.append(f'<span class="command-comment">{line}</span>')
                else:
                    highlighted_cmd.append(line)
            command_text = '\n'.join(highlighted_cmd)

            command_html = f"""
            <div class="command-container">
                <div class="command-header">Example Commands</div>
                <pre class="command-text">{command_text}</pre>
            </div>
            """
        # Map icon name to Feather/Lucide-like SVG paths (simplified)
        icons_svg = {
            "git-branch": '<path d="M6 3v12"></path><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><path d="M18 9a9 9 0 0 1-9 9"></path>',
            "settings": '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
            "refresh-cw": '<polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>',
            "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>',
            "eye-off": '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>',
            "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
            "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>',
            "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline>',
            "terminal": '<polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line>',
            "cpu": '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="15" x2="23" y2="15"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="15" x2="4" y2="15"></line>',
            "anchor": '<circle cx="12" cy="5" r="3"></circle><line x1="12" y1="22" x2="12" y2="8"></line><path d="M5 12H2a10 10 0 0 0 20 0h-3"></path>',
            "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>',
            "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>',
            "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>',
            "lock": '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>',
            "plus-square": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line>',
            "database": '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>',
            "package": '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>',
            "bug": '<rect x="8" y="2" width="8" height="14" rx="4"></rect><path d="M6 7h12M6 11h12M9 16l3 4 3-4M12 2v2"></path>',
            "code": '<polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline>',
            "layout": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line>',
            "copy": '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>',
            "refresh-ccw": '<polyline points="1 4 1 10 7 10"></polyline><polyline points="23 20 23 14 17 14"></polyline><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>',
            "git-pull-request": '<circle cx="18" cy="18" r="3"></circle><circle cx="6" cy="6" r="3"></circle><path d="M13 6h3a2 2 0 0 1 2 2v7"></path><line x1="6" y1="9" x2="6" y2="21"></line>',
            "alert-triangle": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>',
            "clock": '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>',
            "monitor": '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line>',
            "figma": '<path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"></path><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"></path><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"></path><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"></path><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"></path>',
            "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>',
            "wind": '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"></path>',
            "component": '<polygon points="12 2 22 7 12 12 2 7 12 2"></polygon><polygon points="12 12 22 17 12 22 2 17 12 12"></polygon>',
            "sidebar": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line>',
            "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
            "smartphone": '<rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line>',
            "edit-3": '<path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>',
            "check-square": '<polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>',
            "target": '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>',
            "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>',
            "trash-2": '<polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line>',
            "fast-forward": '<polygon points="13 19 22 12 13 5 13 19"></polygon><polygon points="2 19 11 12 2 5 2 19"></polygon>',
            "json": '<polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline><line x1="12" y1="2" x2="12" y2="22"></line>',
            "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>',
            "shuffle": '<polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line>',
            "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>',
            "link-2": '<path d="M15 7h3a5 5 0 0 1 5 5 5 5 0 0 1-5 5h-3m-6 0H6a5 5 0 0 1-5-5 5 5 0 0 1 5-5h3"></path><line x1="8" y1="12" x2="16" y2="12"></line>',
            "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline>',
            "image": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline>',
            "grid": '<rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>',
            "server": '<rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line>',
            "cloud-lightning": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9"></path><polyline points="13 11 9 17 15 17 11 23"></polyline>',
            "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>',
            "help-circle": '<circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line>',
            "info": '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
        }

        icon_svg = icons_svg.get(icon_name, icons_svg['info'])

        html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {s['day_num']} - Slide {s['slide_num']}</title>
    <style>
        {css}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="part-title">{s['part_title']}</div>
            <div class="day-title">วันที่ {s['day_num']}: {s['day_title']}</div>
        </div>
    </header>
    <main>
        <div class="slide-container">
            <span class="slide-number">Slide {s['slide_num']}</span>
            <h1>{s['content']}</h1>

            <div class="info-container">
                <div class="info-text">
                    {details['info']}
                </div>
                <div class="info-icon">
                    <svg width="100%" height="100%" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                        {icon_svg}
                    </svg>
                </div>
            </div>

            {command_html}
        </div>
    </main>
    <div class="nav-buttons">
        <a href="{prev_link}" class="btn {prev_class}">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
            Previous
        </a>
        <a href="../index.html" class="btn">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
            Home
        </a>
        <a href="{next_link}" class="btn btn-primary {next_class}">
            Next
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </a>
    </div>
    <footer>วิทยากร: นายสัจพงศ์ พงศ์ธีรโชติกุล | &copy; 2026 Seminar Series</footer>
</body>
</html>
"""
        with open(f"slides/{filename}", 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == "__main__":
    data = parse_plan('plan.txt')
    generate_slides(data)
    print("Generated index.html and slides/ folder.")
