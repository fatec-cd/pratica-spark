#!/usr/bin/env python3
"""Shared Spark environment checks for the lab scripts."""

import os
import re
import shutil
import subprocess
import sys


SUPPORTED_JAVA_MAJORS = {11, 17}
MIN_PYTHON_VERSION = (3, 8)
MAX_PYTHON_VERSION = (3, 11)


def _java_major(java_executable):
    try:
        completed = subprocess.run(
            [java_executable, "-XshowSettings:properties", "-version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    output = f"{completed.stdout}\n{completed.stderr}"
    match = re.search(r"java\.specification\.version\s*=\s*([0-9]+)(?:\.([0-9]+))?", output)
    if not match:
        return None

    major = int(match.group(1))
    if major == 1 and match.group(2):
        return int(match.group(2))
    return major


def _java_bin(java_home):
    if not java_home:
        return None
    executable = "java.exe" if os.name == "nt" else "java"
    return os.path.join(java_home, "bin", executable)


def _set_java_home(java_home):
    java_bin_dir = os.path.join(java_home, "bin")
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = os.pathsep.join([java_bin_dir, os.environ.get("PATH", "")])


def configure_java_for_spark():
    """Use Java 11 or 17 when available, which matches this Spark 3.5 lab."""
    candidate_homes = [
        os.environ.get("JAVA_HOME"),
        "/usr/lib/jvm/msopenjdk-17-amd64",
        "/usr/lib/jvm/java-17-openjdk-amd64",
        "/usr/lib/jvm/msopenjdk-11-amd64",
        "/usr/lib/jvm/java-11-openjdk-amd64",
    ]

    for java_home in candidate_homes:
        java_executable = _java_bin(java_home)
        if java_executable and os.path.exists(java_executable):
            major = _java_major(java_executable)
            if major in SUPPORTED_JAVA_MAJORS:
                _set_java_home(java_home)
                return major

    java_executable = shutil.which("java")
    if java_executable:
        major = _java_major(java_executable)
        if major in SUPPORTED_JAVA_MAJORS:
            return major
        if major is not None:
            raise RuntimeError(
                "Java {major} detectado. Este roteiro usa Spark 3.5/Hadoop e deve ser "
                "executado com Java 11 ou 17. No Codespaces, recrie o ambiente apos "
                "esta correcao ou execute ./init-repo.sh para instalar o OpenJDK 17."
                .format(major=major)
            )

    raise RuntimeError(
        "Java nao encontrado. Instale o OpenJDK 17 e execute novamente o script de setup."
    )


def configure_python_for_spark():
    version = sys.version_info[:2]
    if version < MIN_PYTHON_VERSION or version > MAX_PYTHON_VERSION:
        raise RuntimeError(
            "Python {major}.{minor} detectado. Este roteiro usa PySpark 3.5.x e deve "
            "ser executado com Python 3.8 a 3.11, preferencialmente Python 3.11 no "
            "Codespaces.".format(major=version[0], minor=version[1])
        )

    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)


def local_spark_builder(app_name, driver_memory="2g", executor_memory=None, shuffle_partitions="4"):
    configure_java_for_spark()
    configure_python_for_spark()

    from pyspark.sql import SparkSession

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", driver_memory)
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
    )

    if executor_memory:
        builder = builder.config("spark.executor.memory", executor_memory)

    return builder