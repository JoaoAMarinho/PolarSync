#!/bin/bash

echo "🚀 Setting up the project..."

# 1️⃣ Create and activate a virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

echo "🔍 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# 2️⃣ Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📜 Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found. Skipping dependency installation."
fi

# 3️⃣ Set up Git hooks
if [ -d "git-hooks" ]; then
    echo "🔗 Configuring Git hooks..."
    git config core.hooksPath git-hooks
else
    echo "⚠️ No 'git-hooks' directory found. Skipping Git hooks setup."
fi

echo "🎉 Setup complete! You can now start working on your project."
