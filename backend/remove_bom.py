# Script to remove BOM from health module's __init__.py file
with open('app/modules/health/__init__.py', 'r', encoding='utf-8-sig') as f:
    content = f.read()

with open('app/modules/health/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('BOM removed successfully from health module __init__.py')