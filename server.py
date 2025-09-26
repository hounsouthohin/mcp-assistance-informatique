#!/usr/bin/env python3
"""
Serveur MCP pour assistance informatique
Expose plusieurs outils utiles pour le diagnostic et la maintenance système
"""

import asyncio
import json
import logging
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
import psutil
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-it-assistant")

# Initialisation du serveur MCP
server = Server("it-assistant")

@server.list_tools()
async def list_tools() -> List[types.Tool]:
    """Liste tous les outils disponibles."""
    return [
        types.Tool(
            name="search_web",
            description="Recherche d'informations sur le web",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Terme de recherche"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Nombre maximum de résultats (défaut: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="calculator",
            description="Calculatrice pour opérations mathématiques",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Expression mathématique à évaluer (ex: 2+2, sqrt(16), sin(3.14159/2))"
                    }
                },
                "required": ["expression"]
            }
        ),
        types.Tool(
            name="system_info",
            description="Obtient des informations sur le système",
            inputSchema={
                "type": "object",
                "properties": {
                    "info_type": {
                        "type": "string",
                        "enum": ["general", "cpu", "memory", "disk", "network", "processes"],
                        "description": "Type d'information système à récupérer"
                    }
                },
                "required": ["info_type"]
            }
        ),
        types.Tool(
            name="ping_host",
            description="Teste la connectivité réseau vers un hôte",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "Adresse IP ou nom d'hôte à pinger"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Nombre de pings à envoyer (défaut: 4)",
                        "default": 4
                    }
                },
                "required": ["host"]
            }
        ),
        types.Tool(
            name="read_file",
            description="Lit le contenu d'un fichier texte",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Chemin vers le fichier à lire"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Encodage du fichier (défaut: utf-8)",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="http_request",
            description="Exécute une requête HTTP",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL de la requête"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE", "HEAD"],
                        "description": "Méthode HTTP (défaut: GET)",
                        "default": "GET"
                    },
                    "headers": {
                        "type": "object",
                        "description": "En-têtes HTTP optionnels"
                    },
                    "data": {
                        "type": "string",
                        "description": "Corps de la requête (pour POST/PUT)"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="port_scan",
            description="Scanne les ports ouverts sur un hôte",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "Adresse IP ou nom d'hôte à scanner"
                    },
                    "ports": {
                        "type": "string",
                        "description": "Ports à scanner (ex: '22,80,443' ou '1-1000')",
                        "default": "22,23,25,53,80,110,443,993,995"
                    }
                },
                "required": ["host"]
            }
        ),
        types.Tool(
            name="log_analysis",
            description="Analyse les logs système",
            inputSchema={
                "type": "object",
                "properties": {
                    "log_file": {
                        "type": "string",
                        "description": "Chemin vers le fichier de log à analyser"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Pattern de recherche (regex supportée)"
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Nombre de lignes à analyser depuis la fin (défaut: 100)",
                        "default": 100
                    }
                },
                "required": ["log_file", "pattern"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Exécute un outil spécifique."""
    try:
        if name == "search_web":
            return await search_web(arguments)
        elif name == "calculator":
            return await calculator(arguments)
        elif name == "system_info":
            return await system_info(arguments)
        elif name == "ping_host":
            return await ping_host(arguments)
        elif name == "read_file":
            return await read_file(arguments)
        elif name == "http_request":
            return await http_request(arguments)
        elif name == "port_scan":
            return await port_scan(arguments)
        elif name == "log_analysis":
            return await log_analysis(arguments)
        else:
            raise ValueError(f"Outil inconnu: {name}")
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de {name}: {e}")
        return [types.TextContent(type="text", text=f"Erreur: {str(e)}")]

async def search_web(args: Dict[str, Any]) -> List[types.TextContent]:
    """Effectue une recherche web basique."""
    query = args["query"]
    max_results = args.get("max_results", 5)
    
    # Simulation d'une recherche web (remplacer par une vraie API)
    results = f"""Résultats de recherche pour "{query}":

1. Documentation officielle - https://docs.example.com/{query.replace(' ', '-')}
2. Stack Overflow - Questions relatives à {query}
3. GitHub - Projets open source sur {query}
4. Tutorial - Guide complet pour {query}
5. Blog technique - Meilleures pratiques {query}

Note: Il s'agit d'une simulation. Pour une vraie recherche, intégrer une API comme DuckDuckGo ou Google."""
    
    return [types.TextContent(type="text", text=results)]

async def calculator(args: Dict[str, Any]) -> List[types.TextContent]:
    """Calculatrice sécurisée."""
    expression = args["expression"]
    
    try:
        # Import des fonctions mathématiques sécurisées
        import math
        
        # Dictionnaire des fonctions autorisées
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pow": pow, "pi": math.pi, "e": math.e
        }
        
        # Évaluation sécurisée
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        
        return [types.TextContent(
            type="text", 
            text=f"Résultat de '{expression}' = {result}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur de calcul: {str(e)}"
        )]

async def system_info(args: Dict[str, Any]) -> List[types.TextContent]:
    """Récupère les informations système."""
    info_type = args["info_type"]
    
    try:
        if info_type == "general":
            info = f"""Informations générales du système:
- OS: {platform.system()} {platform.release()}
- Architecture: {platform.machine()}
- Processeur: {platform.processor()}
- Nom d'hôte: {platform.node()}
- Python: {platform.python_version()}
- Utilisateur: {os.getenv('USER', 'Inconnu')}
- Répertoire de travail: {os.getcwd()}
"""
        
        elif info_type == "cpu":
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = f"""Informations CPU:
- Utilisation: {cpu_percent}%
- Nombre de cœurs: {cpu_count}
- Fréquence: {cpu_freq.current:.2f} MHz (max: {cpu_freq.max:.2f} MHz)
- Temps de fonctionnement: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        elif info_type == "memory":
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            info = f"""Informations mémoire:
- RAM totale: {memory.total / (1024**3):.2f} GB
- RAM utilisée: {memory.used / (1024**3):.2f} GB ({memory.percent}%)
- RAM disponible: {memory.available / (1024**3):.2f} GB
- SWAP total: {swap.total / (1024**3):.2f} GB
- SWAP utilisé: {swap.used / (1024**3):.2f} GB ({swap.percent}%)
"""
        
        elif info_type == "disk":
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            info = f"""Informations disque:
- Espace total: {disk_usage.total / (1024**3):.2f} GB
- Espace utilisé: {disk_usage.used / (1024**3):.2f} GB ({disk_usage.used/disk_usage.total*100:.1f}%)
- Espace libre: {disk_usage.free / (1024**3):.2f} GB
- Lectures: {disk_io.read_count if disk_io else 'N/A'}
- Écritures: {disk_io.write_count if disk_io else 'N/A'}
"""
        
        elif info_type == "network":
            net_io = psutil.net_io_counters()
            interfaces = psutil.net_if_addrs()
            
            info = f"""Informations réseau:
- Bytes envoyés: {net_io.bytes_sent / (1024**2):.2f} MB
- Bytes reçus: {net_io.bytes_recv / (1024**2):.2f} MB
- Paquets envoyés: {net_io.packets_sent}
- Paquets reçus: {net_io.packets_recv}

Interfaces réseau:
"""
            for interface, addrs in interfaces.items():
                info += f"- {interface}: "
                for addr in addrs:
                    if addr.family == 2:  # IPv4
                        info += f"IPv4={addr.address} "
                info += "\n"
        
        elif info_type == "processes":
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Trier par utilisation CPU
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            info = "Top 10 des processus (par CPU):\n"
            for i, proc in enumerate(processes[:10]):
                info += f"{i+1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}% - RAM: {proc['memory_percent']:.1f}%\n"
        
        return [types.TextContent(type="text", text=info)]
    
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors de la récupération des informations système: {str(e)}"
        )]

async def ping_host(args: Dict[str, Any]) -> List[types.TextContent]:
    """Ping un hôte pour tester la connectivité."""
    host = args["host"]
    count = args.get("count", 4)
    
    try:
        # Commande ping selon l'OS
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", str(count), host]
        else:
            cmd = ["ping", "-c", str(count), host]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        output = f"Ping vers {host}:\n\n"
        output += result.stdout
        
        if result.stderr:
            output += f"\nErreurs:\n{result.stderr}"
        
        return [types.TextContent(type="text", text=output)]
    
    except subprocess.TimeoutExpired:
        return [types.TextContent(
            type="text", 
            text=f"Timeout lors du ping vers {host}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors du ping: {str(e)}"
        )]

async def read_file(args: Dict[str, Any]) -> List[types.TextContent]:
    """Lit le contenu d'un fichier."""
    file_path = args["file_path"]
    encoding = args.get("encoding", "utf-8")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return [types.TextContent(
                type="text", 
                text=f"Fichier non trouvé: {file_path}"
            )]
        
        if not path.is_file():
            return [types.TextContent(
                type="text", 
                text=f"Le chemin spécifié n'est pas un fichier: {file_path}"
            )]
        
        # Limite de taille pour éviter les fichiers trop volumineux
        if path.stat().st_size > 1024 * 1024:  # 1MB
            return [types.TextContent(
                type="text", 
                text=f"Fichier trop volumineux (> 1MB): {file_path}"
            )]
        
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        
        result = f"Contenu du fichier '{file_path}':\n\n{content}"
        
        return [types.TextContent(type="text", text=result)]
    
    except UnicodeDecodeError:
        return [types.TextContent(
            type="text", 
            text=f"Erreur d'encodage lors de la lecture de {file_path}. Essayez un autre encodage."
        )]
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors de la lecture du fichier: {str(e)}"
        )]

async def http_request(args: Dict[str, Any]) -> List[types.TextContent]:
    """Exécute une requête HTTP."""
    url = args["url"]
    method = args.get("method", "GET")
    headers = args.get("headers", {})
    data = args.get("data")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                content = await response.text()
                
                result = f"""Requête HTTP {method} vers {url}:
Status: {response.status} {response.reason}
Headers de réponse:
"""
                for key, value in response.headers.items():
                    result += f"  {key}: {value}\n"
                
                result += f"\nContenu (premiers 1000 caractères):\n{content[:1000]}"
                
                if len(content) > 1000:
                    result += f"\n... (contenu tronqué, {len(content)} caractères au total)"
                
                return [types.TextContent(type="text", text=result)]
    
    except asyncio.TimeoutError:
        return [types.TextContent(
            type="text", 
            text=f"Timeout lors de la requête vers {url}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors de la requête HTTP: {str(e)}"
        )]

async def port_scan(args: Dict[str, Any]) -> List[types.TextContent]:
    """Scanne les ports d'un hôte."""
    host = args["host"]
    ports_str = args.get("ports", "22,23,25,53,80,110,443,993,995")
    
    try:
        # Parse les ports
        ports = []
        for part in ports_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        
        # Limite le nombre de ports pour éviter les scans trop longs
        if len(ports) > 100:
            ports = ports[:100]
        
        open_ports = []
        closed_ports = []
        
        for port in ports:
            try:
                # Test de connexion rapide
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port),
                    timeout=2.0
                )
                writer.close()
                await writer.wait_closed()
                open_ports.append(port)
            except:
                closed_ports.append(port)
        
        result = f"Scan de ports pour {host}:\n\n"
        result += f"Ports ouverts ({len(open_ports)}): {', '.join(map(str, open_ports))}\n"
        result += f"Ports fermés ({len(closed_ports)}): {', '.join(map(str, closed_ports[:20]))}"
        
        if len(closed_ports) > 20:
            result += f" ... et {len(closed_ports) - 20} autres"
        
        return [types.TextContent(type="text", text=result)]
    
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors du scan de ports: {str(e)}"
        )]

async def log_analysis(args: Dict[str, Any]) -> List[types.TextContent]:
    """Analyse les logs système."""
    log_file = args["log_file"]
    pattern = args["pattern"]
    lines = args.get("lines", 100)
    
    try:
        import re
        
        path = Path(log_file)
        if not path.exists():
            return [types.TextContent(
                type="text", 
                text=f"Fichier de log non trouvé: {log_file}"
            )]
        
        # Lire les dernières lignes du fichier
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        # Rechercher le pattern
        matches = []
        for i, line in enumerate(recent_lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                matches.append(f"Ligne {len(all_lines) - len(recent_lines) + i}: {line.strip()}")
        
        result = f"Analyse du fichier de log '{log_file}' (dernières {len(recent_lines)} lignes):\n"
        result += f"Pattern recherché: {pattern}\n"
        result += f"Correspondances trouvées: {len(matches)}\n\n"
        
        if matches:
            result += "Lignes correspondantes:\n"
            for match in matches[:50]:  # Limiter à 50 résultats
                result += f"{match}\n"
            
            if len(matches) > 50:
                result += f"\n... et {len(matches) - 50} autres correspondances"
        else:
            result += "Aucune correspondance trouvée."
        
        return [types.TextContent(type="text", text=result)]
    
    except Exception as e:
        return [types.TextContent(
            type="text", 
            text=f"Erreur lors de l'analyse des logs: {str(e)}"
        )]

async def main():
    """Point d'entrée principal du serveur MCP."""
    logger.info("Démarrage du serveur MCP d'assistance informatique...")
    
    # Options de transport
    transport_type = os.getenv("MCP_TRANSPORT", "stdio")
    
    if transport_type == "stdio":
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    else:
        logger.error(f"Type de transport non supporté: {transport_type}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())