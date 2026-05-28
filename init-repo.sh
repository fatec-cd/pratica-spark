#!/bin/bash
# Bash script para inicializar o repositório PySpark no GitHub Codespaces
# Autor: Professor/Instrutor
# Versão: 1.0

echo "========================================"
echo "  SETUP - PySpark Lab Environment"
echo "========================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Verifica se está no Codespaces
if [ "$CODESPACES" = "true" ]; then
    echo -e "${GREEN}✅ Ambiente GitHub Codespaces detectado${NC}"
else
    echo -e "${YELLOW}⚠️  Executando fora do Codespaces${NC}"
fi

echo ""
echo -e "${CYAN}📦 Verificando dependências...${NC}"

# Verifica Python
echo -n "   Python: "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Não encontrado${NC}"
    exit 1
fi

# Verifica Java. Spark 3.5/Hadoop deve rodar com Java 11 ou 17; Java 21+
# pode falhar na inicializacao com erro em org.apache.hadoop.fs.viewfs.ViewFileSystem.
echo -n "   Java: "
JAVA_MAJOR=""
if command -v java &> /dev/null; then
    JAVA_MAJOR=$(java -XshowSettings:properties -version 2>&1 | awk -F= '/java.specification.version/ {gsub(/ /,"",$2); split($2, version, "."); if (version[1] == "1") print version[2]; else print version[1]; exit}')
fi

if [ "$JAVA_MAJOR" = "11" ] || [ "$JAVA_MAJOR" = "17" ]; then
    echo -e "${GREEN}✅ Java $JAVA_MAJOR instalado${NC}"
else
    if [ -n "$JAVA_MAJOR" ]; then
        echo -e "${YELLOW}⚠️  Java $JAVA_MAJOR detectado - instalando OpenJDK 17...${NC}"
    else
        echo -e "${YELLOW}⚠️  Não encontrado - instalando OpenJDK 17...${NC}"
    fi
    sudo apt-get update -qq
    sudo apt-get install -y openjdk-17-jdk -qq
    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
    export PATH="$JAVA_HOME/bin:$PATH"
    echo -e "   ${GREEN}✅ Java 17 configurado${NC}"
fi

echo ""
echo -e "${CYAN}📚 Instalando dependências Python...${NC}"
cd pyspark_app
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}🔧 Configurando ambiente...${NC}"

# Torna scripts executáveis
chmod +x *.py
echo -e "${GREEN}✅ Permissões configuradas${NC}"

# Cria diretórios necessários
mkdir -p data/output
echo -e "${GREEN}✅ Diretórios criados${NC}"

echo ""
echo -e "${CYAN}📊 Gerando dados de exemplo...${NC}"
python3 data_generator.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dados gerados com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao gerar dados${NC}"
    exit 1
fi

echo ""
echo "========================================"
echo -e "${GREEN}✅ Setup concluído com sucesso!${NC}"
echo "========================================"
echo ""
echo -e "${CYAN}📚 Próximos passos:${NC}"
echo "   1. Explore o README.md do projeto"
echo "   2. Execute: cd pyspark_app"
echo "   3. Execute: python3 spark_word_count.py"
echo "   4. Execute: python3 spark_sales_analysis.py"
echo ""
