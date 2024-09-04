is_package_installed() {
    dpkg -l | grep -q "^ii  $1 "
}
if is_package_installed "python3-flask"; then
    echo "Flask ya está instalado."
else
    echo "Instalando dependencia de Flask... Se necesita confirmación"
    sudo apt-get install -y python3-flask
fi

# Instalar nftables si no está instalado
if is_package_installed "nftables"; then
    echo "nftables ya está instalado."
else
    echo "Instalando dependencia de nftables... Se necesita confirmación"
    sudo apt-get install -y nftables
    sudo systemctl start nftables
    sudo systemctl enable nftables
fi

SCRIPT_PATH="$PWD/run_nft_commands.sh"
USER=$(whoami)
sudo chmod +x $SCRIPT_PATH
sudo cp /etc/sudoers /etc/sudoers.bak
echo "$USER ALL=(ALL) NOPASSWD: $SCRIPT_PATH" | sudo tee -a /etc/sudoers > /dev/null