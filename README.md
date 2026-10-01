## 📑 Table of contents 📑
- [Project description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## 💡 Project Description 💡 <a name="project-description"></a>
[**Discord**](https://discord.com) is a cross-platform instant messaging platform with VoIP and video conferencing support.

This Discord bot is written in Python as a pet project and demonstration of development skills. It uses models provided through [**gpt4free**](https://github.com/xtekky/gpt4free) and Hugging Face Spaces.

## 🚀 Features 🚀 <a name="features"></a>
The following features are available with the GPT4All bot:
- **Slash commands** 📝: Supports `/ask`, `/imagine`, `/whois`, and `/help`.
- **Command `/ask`** 💭: Sends a prompt to the configured GPT model and returns its answer.
- **Command `/imagine`** 🎨: Generates an image from a prompt using a supported Hugging Face Space.
- **Command `/whois`** 🤔: Lists members of the current server who have the selected role.
- **Command `/help`** 🆘: Displays information about the available commands, developers, and project repository.

## 🛠 Installation 🛠 <a name="installation"></a>
1. Install Python and clone this repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add the Discord bot token:

   ```dotenv
   DISCORD_TOKEN=your_token_here
   ```

4. Enable the required Discord intents for the bot and run:

   ```bash
   python main.py
   ```

## 🤝 Contributing 🤝 <a name="contributing"></a>
Contributions are welcome. Open an issue or pull request describing the proposed change.

## 📝 License 📝 <a name="license"></a>
This project is licensed under the [MIT License](./LICENSE).
