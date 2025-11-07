#!/bin/bash

# Script para configurar permissões do Docker no GitHub Codespaces
# Uso: bash setup-docker-permissions.sh

echo "🔧 Configurando permissões do Docker..."

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Certifique-se de que o Docker está instalado."
    exit 1
fi

# Adiciona o usuário ao grupo docker
echo "📝 Adicionando usuário ao grupo docker..."
sudo usermod -aG docker $USER

# Verifica se o grupo foi adicionado
if groups $USER | grep -q docker; then
    echo "✅ Usuário adicionado ao grupo docker com sucesso!"
else
    echo "⚠️  Aviso: Pode ser necessário reiniciar o Codespace para aplicar as mudanças."
fi

# Ativa o novo grupo (sem precisar fazer logout/login)
echo "🔄 Ativando novo grupo..."
newgrp docker << EONG
    echo "🧪 Testando acesso ao Docker..."
    docker ps &> /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Docker configurado com sucesso!"
        echo "🚀 Você já pode executar comandos Docker sem sudo!"
    else
        echo "⚠️  Ainda há problemas de permissão."
        echo "💡 Tente reiniciar o Codespace:"
        echo "   - Clique nos três pontos (...) no canto superior"
        echo "   - Selecione 'Restart Codespace'"
    fi
EONG

echo ""
echo "📋 Teste rápido:"
echo "   docker ps"
echo "   docker images"
echo ""
echo "Se ainda houver erro, reinicie o Codespace."
