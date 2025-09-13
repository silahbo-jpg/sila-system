#!/usr/bin/env python3
"""
Script to test the protocol flow (deferimento/indeferimento/reenvio) for complaints.
"""
import psycopg2
import random
from datetime import datetime, timedelta
import os

def connect_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'sila_db'),
        user=os.getenv('DB_USER', 'sila_user'),
        password=os.getenv('DB_PASSWORD', 'sila_password')
    )
    return conn

def get_random_complaint(conn, status=None):
    """Get a random complaint from the database, optionally filtered by status."""
    cursor = conn.cursor()
    
    if status:
        cursor.execute("SELECT * FROM \"Complaint\" WHERE status = %s ORDER BY RANDOM() LIMIT 1", (status,))
    else:
        cursor.execute("SELECT * FROM \"Complaint\" ORDER BY RANDOM() LIMIT 1")
    
    complaint = cursor.fetchone()
    if complaint:
        # Get column names
        colnames = [desc[0] for desc in cursor.description]
        return dict(zip(colnames, complaint))
    return None

def update_complaint_status(conn, complaint_id, new_status, user_id, comment=None):
    """Update the status of a complaint and add a comment."""
    cursor = conn.cursor()
    now = datetime.now()
    
    try:
        # Update the complaint status
        cursor.execute(
            "UPDATE \"Complaint\" SET status = %s, updated_at = %s WHERE id = %s",
            (new_status, now, complaint_id)
        )
        
        # Add a comment about the status change
        if comment is None:
            status_text = {
                'pendente': 'enviada para análise',
                'em_analise': 'em análise',
                'deferida': 'deferida',
                'indeferida': 'indeferida',
                'encaminhada': 'encaminhada para outro setor',
                'concluida': 'concluída',
                'rejeitada': 'rejeitada'
            }.get(new_status, 'atualizada')
            
            comment = f"Status alterado para '{status_text}' por usuário {user_id}"
        
        cursor.execute(
            """
            INSERT INTO \"ComplaintComment\" (\"complaintId\", \"userId\", content, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (complaint_id, user_id, comment, now)
        )
        
        conn.commit()
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to update complaint status: {e}")
        conn.rollback()
        return False

def test_deferimento(conn, complaint_id, user_id):
    """Test the deferimento (approval) flow for a complaint."""
    print(f"\n🔵 Testando fluxo de DEFERIMENTO para reclamação {complaint_id}")
    
    # Change status to 'em_analise' if not already
    update_complaint_status(conn, complaint_id, 'em_analise', user_id, 
                          "Reclamação em análise pelo setor responsável.")
    
    # Approve the complaint
    success = update_complaint_status(
        conn, complaint_id, 'deferida', user_id,
        "Reclamação deferida. O caso será encaminhado para resolução."
    )
    
    if success:
        print(f"  ✅ Reclamação {complaint_id} deferida com sucesso!")
    else:
        print(f"  ❌ Falha ao deferir reclamação {complaint_id}")
    
    return success

def test_indeferimento(conn, complaint_id, user_id, motivo):
    """Test the indeferimento (rejection) flow for a complaint."""
    print(f"\n🔴 Testando fluxo de INDEFERIMENTO para reclamação {complaint_id}")
    
    # Change status to 'em_analise' if not already
    update_complaint_status(conn, complaint_id, 'em_analise', user_id, 
                          "Reclamação em análise pelo setor responsável.")
    
    # Reject the complaint
    success = update_complaint_status(
        conn, complaint_id, 'indeferida', user_id,
        f"Reclamação indeferida. Motivo: {motivo}"
    )
    
    if success:
        print(f"  ✅ Reclamação {complaint_id} indeferida com sucesso!")
    else:
        print(f"  ❌ Falha ao indeferir reclamação {complaint_id}")
    
    return success

def test_reenvio(conn, complaint_id, user_id, novo_setor):
    """Test the reenvio (forwarding) flow for a complaint."""
    print(f"\n🔄 Testando fluxo de REENVIO para reclamação {complaint_id}")
    
    # Change status to 'em_analise' if not already
    update_complaint_status(conn, complaint_id, 'em_analise', user_id, 
                          "Reclamação em análise pelo setor responsável.")
    
    # Forward the complaint
    success = update_complaint_status(
        conn, complaint_id, 'encaminhada', user_id,
        f"Reclamação encaminhada para o setor: {novo_setor}"
    )
    
    if success:
        print(f"  ✅ Reclamação {complaint_id} encaminhada para {novo_setor} com sucesso!")
    else:
        print(f"  ❌ Falha ao encaminhar reclamação {complaint_id}")
    
    return success

def main():
    """Main function to test the protocol flow."""
    print("🚀 Iniciando testes de fluxo de protocolo")
    
    try:
        conn = connect_db()
        
        # Get postgres postgres ID (postgres with is_superuser = true)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM postgres WHERE is_superuser = true LIMIT 1")
        admin_user = cursor.fetchone()
        
        if not admin_user:
            print("❌ Nenhum usuário administrador encontrado!")
            return
        
        admin_id = admin_user[0]
        print(f"  Usuário administrador: ID {admin_id}")
        
        # Get a random complaint to test with
        complaint = get_random_complaint(conn)
        if not complaint:
            print("❌ Nenhuma reclamação encontrada no banco de dados!")
            return
        
        print(f"\n🔍 Reclamação selecionada para teste:")
        print(f"  ID: {complaint['id']}")
        print(f"  Título: {complaint['title']}")
        print(f"  Status atual: {complaint['status']}")
        
        # Test deferimento
        test_deferimento(conn, complaint['id'], admin_id)
        
        # Get another complaint for indeferimento test
        cursor.execute("SELECT * FROM \"Complaint\" WHERE status = %s ORDER BY RANDOM() LIMIT 1", ('pendente',))
        complaint = cursor.fetchone()
        if complaint:
            # Get column names
            colnames = [desc[0] for desc in cursor.description]
            complaint_dict = dict(zip(colnames, complaint))
            test_indeferimento(
                conn, 
                complaint_dict['id'], 
                admin_id,
                "Informações insuficientes para análise."
            )
        
        # Get another complaint for reenvio test
        cursor.execute("SELECT * FROM \"Complaint\" WHERE status = %s ORDER BY RANDOM() LIMIT 1", ('pendente',))
        complaint = cursor.fetchone()
        if complaint:
            # Get column names
            colnames = [desc[0] for desc in cursor.description]
            complaint_dict = dict(zip(colnames, complaint))
            setores = ["Saúde", "Educação", "Obras", "Meio Ambiente", "Segurança"]
            test_reenvio(
                conn,
                complaint_dict['id'],
                admin_id,
                random.choice(setores)
            )
        
        print("\n✅ Testes de fluxo de protocolo concluídos!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()