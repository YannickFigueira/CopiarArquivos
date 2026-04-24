# Changelog

## [4.0.0] - 2025-12-16
### Recriado programa para cópia de arquivos
- Arquivo principal `copiararquivos.py`
- Módulo auxiliar `metodos.py`

## [4.0.1] - 2025-12-17
### Changes
- Adicionado criação de log de erros ao copiar arquivos
- Adicionado clipboard com o botão direito do mouse nos textos de origem e destino

### Fixes
- Corrigido para mostras o arquivo que está a copiar no momento e não o que já foi copiado
- Algumas pequenas correções e melhorias no código

## [4.0.2] - 2025-12-18
### Changes
- Adicionado botão para verificar lançamento de versão

## [4.0.3] - 2025-12-18
### Changes
- Feito pequenas melhorias
- Adicionado link para donwload de novas versões

## [4.0.4] - 2025-12-20
### Fixed
- Corrigido falha na cópia de arquivos devido a erro na leitura das pastas
- Alterado o mostrador do tempo decorrido que parava durante a cópia de cada arquivo

## [4.0.5] - 2026-01-16
### Fixed
- Verificação de arquivos já copiados para serem ignorados
- Verificação de arquivos copiados incompletos/corrompidos para serem substituídos
- Corrigido tempo que não reiniciava para a nova cópia sem fechar o programa
- Corrigido falha na execução da cópia quando colado caminho do Windows direto na caixa de texto

## [4.0.6] - 2026-03-29
### Changes
- Ajustado o tempo para mostras as horas corretamente

## [4.0.7] - 2026-04-09
### Changes
- Adicionado tamanho dos arquivos na área de texto
- Adicionado alerta de espaço insuficiente em disco, para liberar espaço e continuar
- Cronometro pausa junto ao alerta de espaço

## [4.0.8] - 2026-04-14
### Fixed
- Corrigido verificação do espaço em disco

### Changes
- Adicionado barra de menus
- removido botão para verificar versão, passado para barra de menu

## [4.0.9] - 2026-04-21
### Fixed
- Corrigido utilização infinita do log de ERRO
- Removido importação errada de biblioteca, causando erro na execução

### Changes
- Adicionado menu para abrir log de ERRO
- Adicionado alerta para erros encontrados durante a cópia