import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- CONFIGURAÇÕES VISUAIS ---
COLOR_BG = "#1a1a1a"
COLOR_CARD = "#262626"
COLOR_GOLD = "#d4af37"   # Monstros
COLOR_TEXT = "#e0e0e0"
COLOR_INPUT = "#3d3d3d"
COLOR_DANGER = "#c0392b" # Cenas/Enredo
COLOR_SUCCESS = "#27ae60" # NPCs
COLOR_BLUE = "#3498db"   # Ambientes
COLOR_PURPLE = "#9b59b6" # Anotações

def init_db():
    conn = sqlite3.connect('grimorio_v23_final.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('CREATE TABLE IF NOT EXISTS cidades (id INTEGER PRIMARY KEY, nome TEXT, tipo TEXT, descricao TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS npcs (id INTEGER PRIMARY KEY, nome TEXT, vinculo TEXT, historia TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS fluxo (id INTEGER PRIMARY KEY, ordem INTEGER, evento TEXT, detalhes TEXT)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS monstros (
                        id INTEGER PRIMARY KEY, nome TEXT, ca INTEGER, pv_max INTEGER,
                        localizacao TEXT, forca TEXT, destreza TEXT, constituicao TEXT, 
                        inteligencia TEXT, sabedoria TEXT, carisma TEXT, notas TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS anotacoes (id INTEGER PRIMARY KEY, titulo TEXT, categoria TEXT, conteudo TEXT)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS painel_ativo (
                        id INTEGER PRIMARY KEY, tipo TEXT, titulo TEXT, 
                        info1 TEXT, info2 TEXT, conteudo TEXT, ordem_painel INTEGER DEFAULT 0, secao INTEGER DEFAULT 0)''')
    conn.commit()
    return conn

class RPGApp:
    def __init__(self, root):
        self.conn = init_db()
        self.root = root
        self.root.title("📜 GRIMÓRIO DO MESTRE v23 - VERSÃO INTEGRAL")
        self.root.geometry("1500x950")
        self.root.configure(bg=COLOR_BG)
        
        self.editing_id = {"npc": None, "cidade": None, "monstro": None, "fluxo": None, "anotacao": None}

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both", padx=10, pady=10)

        # Definição das Abas
        self.aba_home = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_fluxo = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_cidade = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_npc = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_monstros = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_notas = tk.Frame(self.tabs, bg=COLOR_BG)
        self.aba_view = tk.Frame(self.tabs, bg=COLOR_BG)

        self.tabs.add(self.aba_home, text="⚔️ PAINEL ATIVO")
        self.tabs.add(self.aba_fluxo, text="📜 Enredo")
        self.tabs.add(self.aba_cidade, text="🏰 Ambientes")
        self.tabs.add(self.aba_npc, text="👤 NPCs")
        self.tabs.add(self.aba_monstros, text="🐲 Bestiário")
        self.tabs.add(self.aba_notas, text="📓 Anotações")
        self.tabs.add(self.aba_view, text="🗺️ Resumo / Edição")

        self.setup_home(); self.setup_fluxo(); self.setup_cidade(); self.setup_npc()
        self.setup_monstros(); self.setup_notas(); self.setup_view()

    def lbl(self, master, text, color=COLOR_TEXT, size=10, bold=True):
        return tk.Label(master, text=text, bg=master["bg"], fg=color, font=("Segoe UI", size, "bold" if bold else "normal"))

    def ent(self, master, width=20):
        return tk.Entry(master, bg=COLOR_INPUT, fg="white", insertbackground="white", relief="flat", font=("Segoe UI", 10), width=width)

    # --- NOVO: FUNÇÃO PARA EXPANDIR O CARD ---
    def expandir_card(self, tipo, titulo, conteudo, cor):
        top = tk.Toplevel(self.root)
        top.title(f"Visualizar: {titulo}")
        top.geometry("600x700")
        top.configure(bg=COLOR_CARD)
        
        f = tk.Frame(top, bg=COLOR_CARD, padx=20, pady=20)
        f.pack(fill="both", expand=True)
        
        self.lbl(f, f"[{tipo.upper()}]", cor, 12).pack()
        self.lbl(f, titulo.upper(), COLOR_TEXT, 16).pack(pady=10)
        
        txt = tk.Text(f, bg="#111", fg="#fff", font=("Segoe UI", 12), padx=15, pady=15, relief="flat", wrap="word")
        txt.insert("1.0", conteudo)
        txt.config(state="disabled")
        txt.pack(expand=True, fill="both")
        
        tk.Button(f, text="FECHAR", bg=COLOR_DANGER, fg="white", command=top.destroy).pack(pady=10, fill="x")

    def setup_home(self):
        for w in self.aba_home.winfo_children(): w.destroy()
        
        f_ini = tk.Frame(self.aba_home, bg="#111", height=420); f_ini.pack(fill="both", expand=True, pady=5)
        self.lbl(f_ini, "⚔️ ORDEM DE COMBATE (MONSTROS)", COLOR_GOLD, 12).pack(anchor="w", padx=10)
        self.can_ini = tk.Canvas(f_ini, bg="#111", highlightthickness=0); self.scroll_ini = tk.Frame(self.can_ini, bg="#111")
        self.hbar_ini = tk.Scrollbar(f_ini, orient="horizontal", command=self.can_ini.xview); self.can_ini.configure(xscrollcommand=self.hbar_ini.set)
        self.hbar_ini.pack(side="bottom", fill="x"); self.can_ini.pack(fill="both", expand=True); self.can_ini.create_window((0,0), window=self.scroll_ini, anchor="nw")

        f_ref = tk.Frame(self.aba_home, bg="#1a1a1a", height=420); f_ref.pack(fill="both", expand=True, pady=5)
        self.lbl(f_ref, "📌 MUNDO, NPCs E NOTAS", COLOR_BLUE, 12).pack(anchor="w", padx=10)
        self.can_ref = tk.Canvas(f_ref, bg="#1a1a1a", highlightthickness=0); self.scroll_ref = tk.Frame(self.can_ref, bg="#1a1a1a")
        self.hbar_ref = tk.Scrollbar(f_ref, orient="horizontal", command=self.can_ref.xview); self.can_ref.configure(xscrollcommand=self.hbar_ref.set)
        self.hbar_ref.pack(side="bottom", fill="x"); self.can_ref.pack(fill="both", expand=True); self.can_ref.create_window((0,0), window=self.scroll_ref, anchor="nw")
        
        self.atualizar_painel_ui()

    def atualizar_painel_ui(self):
        for w in self.scroll_ini.winfo_children(): w.destroy()
        for w in self.scroll_ref.winfo_children(): w.destroy()
        cores_funcao = {"Monstro": COLOR_GOLD, "Local": COLOR_BLUE, "NPC": COLOR_SUCCESS, "Cena": COLOR_DANGER, "Nota": COLOR_PURPLE}
        itens = self.conn.execute("SELECT * FROM painel_ativo ORDER BY ordem_painel ASC").fetchall()
        for pid, tipo, titulo, i1, i2, cont, ordem, secao in itens:
            cor = cores_funcao.get(tipo, COLOR_TEXT); target = self.scroll_ini if secao == 0 else self.scroll_ref
            card = tk.Frame(target, bg=COLOR_CARD, highlightbackground=cor, highlightthickness=3, width=350, height=450)
            card.pack_propagate(False); card.pack(side="left", padx=15, pady=10)
            
            ctrl = tk.Frame(card, bg="#333"); ctrl.pack(fill="x")
            tk.Button(ctrl, text="←", bg="#444", fg="white", command=lambda id=pid: self.mover_card(id, -1)).pack(side="left", padx=2)
            
            # BOTÃO DE VISUALIZAÇÃO
            tk.Button(ctrl, text="🔍 VER", bg="#444", fg="white", font=("Segoe UI", 8, "bold"), 
                      command=lambda t=tipo, tit=titulo, c=cont, co=cor: self.expandir_card(t, tit, c, co)).pack(side="left", padx=2)
            
            tk.Button(ctrl, text="REMOVER", bg=COLOR_DANGER, fg="white", font=("Segoe UI", 8, "bold"), command=lambda id=pid: self.remover_painel(id)).pack(side="left", expand=True, fill="x", padx=5)
            tk.Button(ctrl, text="→", bg="#444", fg="white", command=lambda id=pid: self.mover_card(id, 1)).pack(side="right", padx=2)
            
            self.lbl(card, f"[{tipo.upper()}]", cor, 9).pack(); self.lbl(card, titulo.upper(), COLOR_TEXT, 11).pack()
            if tipo == "Monstro":
                pv_f = tk.Frame(card, bg=COLOR_CARD); pv_f.pack(pady=5)
                self.lbl(pv_f, f"HP: {i1} / {i2}", COLOR_SUCCESS, 12).pack(side="left", padx=10)
                tk.Button(pv_f, text="-1", command=lambda id=pid: self.ajustar_pv(id, -1)).pack(side="left")
                tk.Button(pv_f, text="+1", command=lambda id=pid: self.ajustar_pv(id, 1)).pack(side="left", padx=2)
            
            txt = tk.Text(card, bg="#1e1e1e", fg="#ccc", font=("Segoe UI", 10), padx=10, pady=10, relief="flat", wrap="word")
            txt.insert("1.0", cont); txt.config(state="disabled"); txt.pack(expand=True, fill="both", padx=5, pady=5)
            
        self.scroll_ini.update_idletasks(); self.can_ini.config(scrollregion=self.can_ini.bbox("all"))
        self.scroll_ref.update_idletasks(); self.can_ref.config(scrollregion=self.can_ref.bbox("all"))

    # --- GESTÃO DE DADOS (ABAS) ---
    def setup_fluxo(self):
        f = tk.Frame(self.aba_fluxo, bg=COLOR_BG, padx=30, pady=20); f.pack(fill="both")
        self.lbl(f, "ORDEM/CAPÍTULO:").pack(anchor="w"); self.ef_o = self.ent(f, 10); self.ef_o.pack(anchor="w")
        self.lbl(f, "TÍTULO DO EVENTO:").pack(anchor="w"); self.ef_t = self.ent(f, 50); self.ef_t.pack(fill="x")
        self.lbl(f, "DESCRIÇÃO DA CENA:").pack(anchor="w"); self.tf_d = tk.Text(f, height=12, bg=COLOR_INPUT, fg="white"); self.tf_d.pack(fill="x", pady=10)
        btns = tk.Frame(f, bg=COLOR_BG); btns.pack(fill="x")
        tk.Button(btns, text="💾 SALVAR ENREDO", bg=COLOR_SUCCESS, command=self.salvar_fluxo).pack(side="left", expand=True, fill="x")
        tk.Button(btns, text="🗑️ EXCLUIR", bg=COLOR_DANGER, command=lambda: self.excluir_db("fluxo", "fluxo")).pack(side="left", padx=5)

    def salvar_fluxo(self):
        v = (self.ef_o.get(), self.ef_t.get(), self.tf_d.get("1.0", tk.END).strip())
        if self.editing_id["fluxo"]: self.conn.execute("UPDATE fluxo SET ordem=?, evento=?, detalhes=? WHERE id=?", (*v, self.editing_id["fluxo"]))
        else: self.conn.execute("INSERT INTO fluxo (ordem, evento, detalhes) VALUES (?,?,?)", v)
        self.conn.commit(); self.carregar_view(); self.editing_id["fluxo"] = None

    def setup_cidade(self):
        f = tk.Frame(self.aba_cidade, bg=COLOR_BG, padx=30, pady=20); f.pack(fill="both")
        self.lbl(f, "NOME DO AMBIENTE:").pack(anchor="w"); self.ec_n = self.ent(f); self.ec_n.pack(fill="x")
        self.lbl(f, "TIPO:").pack(anchor="w"); self.cc_t = ttk.Combobox(f, values=["Masmorra", "Cidade", "Floresta", "Taverna", "Ruínas"]); self.cc_t.pack(fill="x")
        self.lbl(f, "DESCRIÇÃO DO LOCAL:").pack(anchor="w"); self.tc_d = tk.Text(f, height=12, bg=COLOR_INPUT, fg="white"); self.tc_d.pack(fill="x", pady=10)
        btns = tk.Frame(f, bg=COLOR_BG); btns.pack(fill="x")
        tk.Button(btns, text="🏰 SALVAR AMBIENTE", bg=COLOR_SUCCESS, command=self.salvar_cidade).pack(side="left", expand=True, fill="x")
        tk.Button(btns, text="🗑️ EXCLUIR", bg=COLOR_DANGER, command=lambda: self.excluir_db("cidades", "cidade")).pack(side="left", padx=5)

    def salvar_cidade(self):
        v = (self.ec_n.get(), self.cc_t.get(), self.tc_d.get("1.0", tk.END).strip())
        if self.editing_id["cidade"]: self.conn.execute("UPDATE cidades SET nome=?, tipo=?, descricao=? WHERE id=?", (*v, self.editing_id["cidade"]))
        else: self.conn.execute("INSERT INTO cidades (nome, tipo, descricao) VALUES (?,?,?)", v)
        self.conn.commit(); self.carregar_view(); self.editing_id["cidade"] = None

    def setup_npc(self):
        f = tk.Frame(self.aba_npc, bg=COLOR_BG, padx=30, pady=20); f.pack(fill="both")
        self.lbl(f, "NOME DO NPC:").pack(anchor="w"); self.en_n = self.ent(f); self.en_n.pack(fill="x")
        self.lbl(f, "VÍNCULO/PAPEL:").pack(anchor="w"); self.cn_v = ttk.Combobox(f, values=["Aliado", "Inimigo", "Neutro", "Doador de Quest"]); self.cn_v.pack(fill="x")
        self.lbl(f, "HISTÓRIA / PERSONALIDADE:").pack(anchor="w"); self.tn_h = tk.Text(f, height=12, bg=COLOR_INPUT, fg="white"); self.tn_h.pack(fill="x", pady=10)
        btns = tk.Frame(f, bg=COLOR_BG); btns.pack(fill="x")
        tk.Button(btns, text="👤 SALVAR NPC", bg=COLOR_SUCCESS, command=self.salvar_npc).pack(side="left", expand=True, fill="x")
        tk.Button(btns, text="🗑️ EXCLUIR", bg=COLOR_DANGER, command=lambda: self.excluir_db("npcs", "npc")).pack(side="left", padx=5)

    def salvar_npc(self):
        v = (self.en_n.get(), self.cn_v.get(), self.tn_h.get("1.0", tk.END).strip())
        if self.editing_id["npc"]: self.conn.execute("UPDATE npcs SET nome=?, vinculo=?, historia=? WHERE id=?", (*v, self.editing_id["npc"]))
        else: self.conn.execute("INSERT INTO npcs (nome, vinculo, historia) VALUES (?,?,?)", v)
        self.conn.commit(); self.carregar_view(); self.editing_id["npc"] = None

    def setup_monstros(self):
        f = tk.Frame(self.aba_monstros, bg=COLOR_BG, padx=30, pady=20); f.pack(fill="both")
        h = tk.Frame(f, bg=COLOR_BG); h.pack(fill="x")
        self.lbl(h, "NOME:").grid(row=0, column=0); self.em_n = self.ent(h, 25); self.em_n.grid(row=0, column=1, padx=5)
        self.lbl(h, "PV:").grid(row=0, column=2); self.em_p = self.ent(h, 6); self.em_p.grid(row=0, column=3, padx=5)
        self.lbl(h, "CA:").grid(row=0, column=4); self.em_c = self.ent(h, 6); self.em_c.grid(row=0, column=5, padx=5)
        self.lbl(f, "🗺️ LOCALIZAÇÃO:").pack(anchor="w", pady=(10,0)); self.em_loc = self.ent(f, 40); self.em_loc.pack(fill="x")
        attr_f = tk.Frame(f, bg=COLOR_BG); attr_f.pack(pady=10)
        self.m_attrs = {}
        for i, a in enumerate(["FOR", "DES", "CON", "INT", "SAB", "CAR"]):
            self.lbl(attr_f, a).grid(row=0, column=i*2); e = self.ent(attr_f, 5); e.grid(row=0, column=i*2+1, padx=2); self.m_attrs[a] = e
        self.lbl(f, "NOTAS DE COMBATE:").pack(anchor="w"); self.tm_n = tk.Text(f, height=8, bg=COLOR_INPUT, fg="white"); self.tm_n.pack(fill="x", pady=10)
        btns = tk.Frame(f, bg=COLOR_BG); btns.pack(fill="x")
        tk.Button(btns, text="🐲 SALVAR MONSTRO", bg=COLOR_SUCCESS, command=self.salvar_monstro).pack(side="left", expand=True, fill="x")
        tk.Button(btns, text="🗑️ EXCLUIR", bg=COLOR_DANGER, command=lambda: self.excluir_db("monstros", "monstro")).pack(side="left", padx=5)

    def salvar_monstro(self):
        v = (self.em_n.get(), self.em_c.get(), self.em_p.get(), self.em_loc.get(), self.m_attrs["FOR"].get(), self.m_attrs["DES"].get(), self.m_attrs["CON"].get(), self.m_attrs["INT"].get(), self.m_attrs["SAB"].get(), self.m_attrs["CAR"].get(), self.tm_n.get("1.0", tk.END).strip())
        if self.editing_id["monstro"]: self.conn.execute("UPDATE monstros SET nome=?, ca=?, pv_max=?, localizacao=?, forca=?, destreza=?, constituicao=?, inteligencia=?, sabedoria=?, carisma=?, notas=? WHERE id=?", (*v, self.editing_id["monstro"]))
        else: self.conn.execute("INSERT INTO monstros (nome, ca, pv_max, localizacao, forca, destreza, constituicao, inteligencia, sabedoria, carisma, notas) VALUES (?,?,?,?,?,?,?,?,?,?,?)", v)
        self.conn.commit(); self.carregar_view(); self.editing_id["monstro"] = None

    def setup_notas(self):
        f = tk.Frame(self.aba_notas, bg=COLOR_BG, padx=30, pady=20); f.pack(fill="both")
        self.lbl(f, "TÍTULO:").pack(anchor="w"); self.ea_t = self.ent(f, 50); self.ea_t.pack(fill="x")
        self.lbl(f, "CATEGORIA:").pack(anchor="w", pady=(10,0)); self.ea_c = self.ent(f, 30); self.ea_c.pack(fill="x")
        self.lbl(f, "CONTEÚDO:").pack(anchor="w", pady=(10,0)); self.ta_cont = tk.Text(f, height=15, bg=COLOR_INPUT, fg="white"); self.ta_cont.pack(fill="x", pady=10)
        btns = tk.Frame(f, bg=COLOR_BG); btns.pack(fill="x")
        tk.Button(btns, text="📓 SALVAR NOTA", bg=COLOR_PURPLE, fg="white", command=self.salvar_anotacao).pack(side="left", expand=True, fill="x")
        tk.Button(btns, text="🗑️ EXCLUIR", bg=COLOR_DANGER, command=lambda: self.excluir_db("anotacoes", "anotacao")).pack(side="left", padx=5)

    def salvar_anotacao(self):
        v = (self.ea_t.get(), self.ea_c.get(), self.ta_cont.get("1.0", tk.END).strip())
        if self.editing_id["anotacao"]: self.conn.execute("UPDATE anotacoes SET titulo=?, categoria=?, conteudo=? WHERE id=?", (*v, self.editing_id["anotacao"]))
        else: self.conn.execute("INSERT INTO anotacoes (titulo, categoria, conteudo) VALUES (?,?,?)", v)
        self.conn.commit(); self.carregar_view(); self.editing_id["anotacao"] = None

    # --- RESUMO E GESTÃO ---
    def setup_view(self):
        f = tk.Frame(self.aba_view, bg=COLOR_BG, padx=20, pady=20); f.pack(fill="both", expand=True)
        self.e_busca = self.ent(f, 30); self.e_busca.pack(pady=10); self.e_busca.bind("<KeyRelease>", lambda e: self.carregar_view())
        self.tree = ttk.Treeview(f, columns=("ID", "Tipo", "Nome", "Info"), show="headings")
        for col in ("ID", "Tipo", "Nome", "Info"): self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", lambda e: self.spawn_prep())
        self.tree.bind("<Double-1>", lambda e: self.carregar_edicao())

    def carregar_view(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        b = f"%{self.e_busca.get()}%"
        for r in self.conn.execute("SELECT id, 'Local', nome, tipo FROM cidades WHERE nome LIKE ?", (b,)).fetchall(): self.tree.insert("", "end", values=r)
        for r in self.conn.execute("SELECT id, 'NPC', nome, vinculo FROM npcs WHERE nome LIKE ?", (b,)).fetchall(): self.tree.insert("", "end", values=r)
        for r in self.conn.execute("SELECT id, 'Monstro', nome, localizacao FROM monstros WHERE nome LIKE ?", (b,)).fetchall(): self.tree.insert("", "end", values=r)
        for r in self.conn.execute("SELECT id, 'Enredo', evento, ordem FROM fluxo WHERE evento LIKE ?", (b,)).fetchall(): self.tree.insert("", "end", values=r)
        for r in self.conn.execute("SELECT id, 'Nota', titulo, categoria FROM anotacoes WHERE titulo LIKE ?", (b,)).fetchall(): self.tree.insert("", "end", values=r)

    def carregar_edicao(self):
        if not self.tree.selection(): return
        item = self.tree.item(self.tree.selection()[0], 'values')
        db_id, tipo = item[0], item[1]
        if tipo == "Enredo":
            r = self.conn.execute("SELECT * FROM fluxo WHERE id=?", (db_id,)).fetchone()
            self.editing_id["fluxo"] = r[0]; self.ef_o.delete(0,tk.END); self.ef_o.insert(0, r[1]); self.ef_t.delete(0,tk.END); self.ef_t.insert(0, r[2]); self.tf_d.delete("1.0", tk.END); self.tf_d.insert("1.0", r[3]); self.tabs.select(1)
        elif tipo == "Local":
            r = self.conn.execute("SELECT * FROM cidades WHERE id=?", (db_id,)).fetchone()
            self.editing_id["cidade"] = r[0]; self.ec_n.delete(0,tk.END); self.ec_n.insert(0, r[1]); self.cc_t.set(r[2]); self.tc_d.delete("1.0", tk.END); self.tc_d.insert("1.0", r[3]); self.tabs.select(2)
        elif tipo == "NPC":
            r = self.conn.execute("SELECT * FROM npcs WHERE id=?", (db_id,)).fetchone()
            self.editing_id["npc"] = r[0]; self.en_n.delete(0,tk.END); self.en_n.insert(0, r[1]); self.cn_v.set(r[2]); self.tn_h.delete("1.0", tk.END); self.tn_h.insert("1.0", r[3]); self.tabs.select(3)
        elif tipo == "Monstro":
            r = self.conn.execute("SELECT * FROM monstros WHERE id=?", (db_id,)).fetchone()
            self.editing_id["monstro"] = r[0]; self.em_n.delete(0,tk.END); self.em_n.insert(0, r[1]); self.em_c.delete(0,tk.END); self.em_c.insert(0, r[2]); self.em_p.delete(0,tk.END); self.em_p.insert(0, r[3]); self.em_loc.delete(0,tk.END); self.em_loc.insert(0, r[4])
            for i, a in enumerate(["FOR", "DES", "CON", "INT", "SAB", "CAR"]): self.m_attrs[a].delete(0,tk.END); self.m_attrs[a].insert(0, r[5+i])
            self.tm_n.delete("1.0", tk.END); self.tm_n.insert("1.0", r[11]); self.tabs.select(4)
        elif tipo == "Nota":
            r = self.conn.execute("SELECT * FROM anotacoes WHERE id=?", (db_id,)).fetchone()
            self.editing_id["anotacao"] = r[0]; self.ea_t.delete(0,tk.END); self.ea_t.insert(0, r[1]); self.ea_c.delete(0,tk.END); self.ea_c.insert(0, r[2]); self.ta_cont.delete("1.0", tk.END); self.ta_cont.insert("1.0", r[3]); self.tabs.select(5)

    def spawn_prep(self):
        if not self.tree.selection(): return
        db_id, tipo = self.tree.item(self.tree.selection()[0], 'values')[0:2]
        top = tk.Toplevel(self.root, bg=COLOR_CARD); top.geometry("300x150")
        # Centralizar popup em relação à janela principal
        top.transient(self.root) 
        tk.Button(top, text="📌 ENVIAR PARA O PAINEL", bg=COLOR_SUCCESS, fg="white", 
                  padx=10, pady=10, command=lambda: self.adicionar_final(tipo, db_id, top)).pack(expand=True)

    def adicionar_final(self, tipo, db_id, top):
        if tipo == "Monstro":
            r = self.conn.execute("SELECT * FROM monstros WHERE id=?", (db_id,)).fetchone()
            cont = f"LOCAL: {r[4]}\nCA: {r[2]} | FOR:{r[5]} DES:{r[6]} CON:{r[7]}\nINT:{r[8]} SAB:{r[9]} CAR:{r[10]}\n\nNOTAS:\n{r[11]}"
            self.spawn_db("Monstro", r[1], r[3], r[3], cont, 0)
        elif tipo == "Local":
            r = self.conn.execute("SELECT * FROM cidades WHERE id=?", (db_id,)).fetchone()
            self.spawn_db("Local", r[1], "", "", r[3], 1)
        elif tipo == "NPC":
            r = self.conn.execute("SELECT * FROM npcs WHERE id=?", (db_id,)).fetchone()
            self.spawn_db("NPC", r[1], "", "", r[3], 1)
        elif tipo == "Enredo":
            r = self.conn.execute("SELECT * FROM fluxo WHERE id=?", (db_id,)).fetchone()
            self.spawn_db("Cena", r[2], "", "", r[3], 1)
        elif tipo == "Nota":
            r = self.conn.execute("SELECT * FROM anotacoes WHERE id=?", (db_id,)).fetchone()
            self.spawn_db("Nota", r[1], r[2], "", r[3], 1)
        
        # CORREÇÃO DO BUG: Fechar a janela e mudar para a aba Home
        top.destroy() 
        self.tabs.select(0)

    def spawn_db(self, tipo, tit, i1, i2, cont, sec):
        ordem = self.conn.execute("SELECT COUNT(*) FROM painel_ativo WHERE secao=?", (sec,)).fetchone()[0]
        self.conn.execute("INSERT INTO painel_ativo (tipo, titulo, info1, info2, conteudo, ordem_painel, secao) VALUES (?,?,?,?,?,?,?)", (tipo, tit, str(i1), str(i2), cont, ordem, sec))
        self.conn.commit()
        self.atualizar_painel_ui()

    def mover_card(self, pid, d): self.conn.execute("UPDATE painel_ativo SET ordem_painel=ordem_painel+? WHERE id=?", (d, pid)); self.conn.commit(); self.atualizar_painel_ui()
    def ajustar_pv(self, pid, v): self.conn.execute("UPDATE painel_ativo SET info1=CAST(info1 AS INTEGER)+? WHERE id=?", (v, pid)); self.conn.commit(); self.atualizar_painel_ui()
    def remover_painel(self, pid): self.conn.execute("DELETE FROM painel_ativo WHERE id=?", (pid,)); self.conn.commit(); self.atualizar_painel_ui()
    def excluir_db(self, tabela, chave):
        if self.editing_id[chave] and messagebox.askyesno("Excluir", "Apagar permanentemente?"):
            self.conn.execute(f"DELETE FROM {tabela} WHERE id=?", (self.editing_id[chave],))
            self.conn.commit(); self.carregar_view(); self.editing_id[chave] = None

if __name__ == "__main__":
    root = tk.Tk(); app = RPGApp(root); root.mainloop()
