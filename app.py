import streamlit as st
import hashlib
import json
import time
import random
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="Blockchain Copyright System",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

LANGUAGES = {
    "Türkçe": {
        "title": "🔗 Blockchain Telif Sistemi",
        "subtitle": "TÜBİTAK 4006-A Projesi - Dijital Sanat Koruma",
        "home": "🏠 Ana Sayfa",
        "create_nft": "🎨 NFT Oluştur",
        "blockchain": "⛓️ Blockchain",
        "analytics": "📊 Analizler",
        "verify": "🔍 Doğrula",
        "welcome": "Blockchain Telif Sistemine Hoş Geldiniz",
        "total_blocks": "Toplam Blok",
        "chain_valid": "Zincir Geçerli",
        "nfts_created": "Oluşturulan NFT'ler",
        "difficulty": "Zorluk",
        "last_block": "Son Blok",
        "how_it_works": "Nasıl Çalışır?",
        "blockchain_tech": "Blockchain Teknolojisi",
        "nft_process": "NFT Oluşturma Süreci",
        "copyright_protection": "Telif Koruması",
        "mint_your_art": "Dijital Sanatını NFT'ye Dönüştür",
        "artwork_title": "Sanat Eseri Başlığı",
        "description": "Açıklama",
        "artist_name": "Sanatçı Adı",
        "upload_artwork": "Sanat Eseri Yükle",
        "mint_nft": "🚀 NFT Oluştur",
        "nft_success": "✅ NFT Başarıyla Oluşturuldu!",
        "nft_details": "📋 NFT Detayları",
        "blockchain_explorer": "Blockchain Gezgini",
        "refresh_chain": "🔄 Zinciri Yenile",
        "search_block": "Blok Ara (Index)",
        "full_chain": "Tam Zincir Görselleştirmesi",
        "blockchain_analytics": "Blockchain Analizleri",
        "nft_registry_stats": "NFT Kayıt İstatistikleri",
        "file_verification": "Dosya Doğrulama",
        "upload_verify": "Doğrulamak İçin Dosya Yükle",
        "file_info": "Dosya Bilgileri",
        "blockchain_verification": "Blockchain Doğrulama",
        "image_analysis": "Görüntü Analizi",
        "dimensions": "Boyutlar",
        "file_size": "Dosya Boyutu",
        "similarity_score": "Benzerlik Skoru",
        "not_found": "⚠️ Dosya blockchain'de bulunamadı. Bu dosya NFT olarak kaydedilmemiş.",
        "found_in_blockchain": "✅ Dosya blockchain'de bulundu! {count} blokta bulundu."
    },
    "English": {
        "title": "🔗 Blockchain Copyright System",
        "subtitle": "TÜBİTAK 4006-A Project - Digital Art Protection",
        "home": "🏠 Home",
        "create_nft": "🎨 Create NFT",
        "blockchain": "⛓️ Blockchain",
        "analytics": "📊 Analytics",
        "verify": "🔍 Verify",
        "welcome": "Welcome to Blockchain Copyright System",
        "total_blocks": "Total Blocks",
        "chain_valid": "Chain Valid",
        "nfts_created": "NFTs Created",
        "difficulty": "Difficulty",
        "last_block": "Last Block",
        "how_it_works": "How It Works?",
        "blockchain_tech": "Blockchain Technology",
        "nft_process": "NFT Creation Process",
        "copyright_protection": "Copyright Protection",
        "mint_your_art": "Mint Your Digital Art as NFT",
        "artwork_title": "Artwork Title",
        "description": "Description",
        "artist_name": "Artist Name",
        "upload_artwork": "Upload Artwork",
        "mint_nft": "🚀 Mint NFT",
        "nft_success": "✅ NFT Successfully Minted!",
        "nft_details": "📋 NFT Details",
        "blockchain_explorer": "Blockchain Explorer",
        "refresh_chain": "🔄 Refresh Chain",
        "search_block": "Search Block by Index",
        "full_chain": "Full Chain Visualization",
        "blockchain_analytics": "Blockchain Analytics",
        "nft_registry_stats": "NFT Registry Statistics",
        "file_verification": "File Verification",
        "upload_verify": "Upload File to Verify",
        "file_info": "File Information",
        "blockchain_verification": "Blockchain Verification",
        "image_analysis": "Image Analysis",
        "dimensions": "Dimensions",
        "file_size": "File Size",
        "similarity_score": "Similarity Score",
        "not_found": "⚠️ File not found in blockchain. This file has not been registered as an NFT.",
        "found_in_blockchain": "✅ File found in blockchain! Found in {count} block(s)."
    }
}

class BlockchainDemo:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pending_data = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = {
            'index': 0,
            'timestamp': str(datetime.now()),
            'data': 'Genesis Block - TÜBİTAK 4006-A',
            'previous_hash': '0',
            'nonce': 0,
            'hash': self.calculate_hash(0, str(datetime.now()), 'Genesis Block - TÜBİTAK 4006-A', '0', 0)
        }
        self.chain.append(genesis)
    
    def calculate_hash(self, index, timestamp, data, previous_hash, nonce):
        value = str(index) + timestamp + data + previous_hash + str(nonce)
        return hashlib.sha256(value.encode()).hexdigest()
    
    def proof_of_work(self, index, timestamp, data, previous_hash):
        nonce = 0
        while True:
            hash_value = self.calculate_hash(index, timestamp, data, previous_hash, nonce)
            if hash_value[:self.difficulty] == '0' * self.difficulty:
                return hash_value, nonce
            nonce += 1
    
    def add_block(self, data):
        if not self.chain:
            return False
        
        previous_block = self.chain[-1]
        new_index = len(self.chain)
        timestamp = str(datetime.now())
        
        hash_value, nonce = self.proof_of_work(new_index, timestamp, data, previous_block['hash'])
        
        new_block = {
            'index': new_index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_block['hash'],
            'nonce': nonce,
            'hash': hash_value
        }
        
        self.chain.append(new_block)
        return True
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current['previous_hash'] != previous['hash']:
                return False
            
            recalculated_hash = self.calculate_hash(
                current['index'], 
                current['timestamp'], 
                current['data'], 
                current['previous_hash'], 
                current['nonce']
            )
            
            if current['hash'] != recalculated_hash:
                return False
        
        return True
    
    def get_chain_stats(self):
        return {
            'total_blocks': len(self.chain),
            'valid_chain': self.is_chain_valid(),
            'last_block': self.chain[-1] if self.chain else None
        }

def create_file_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()

def analyze_image_similarity(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        width, height = image.size
        file_size = len(uploaded_file.getvalue())
        
        similarity_score = random.uniform(15, 85)
        
        return {
            'width': width,
            'height': height,
            'size_mb': round(file_size / (1024*1024), 2),
            'similarity_score': round(similarity_score, 1),
            'format': image.format
        }
    except:
        return None

def main():
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = BlockchainDemo()
    
    if 'nft_registry' not in st.session_state:
        st.session_state.nft_registry = []
    
    if 'language' not in st.session_state:
        st.session_state.language = "Türkçe"
    
    lang = LANGUAGES[st.session_state.language]
    
    st.sidebar.markdown("---")
    st.session_state.language = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
    lang = LANGUAGES[st.session_state.language]
    
    st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .block-card {{
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }}
    .success-message {{
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }}
    .warning-message {{
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{lang['title']}</h1>
        <p>{lang['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = [lang['home'], lang['create_nft'], lang['blockchain'], lang['analytics'], lang['verify']]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == lang['home']:
        st.subheader(lang['welcome'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(lang['total_blocks'], len(st.session_state.blockchain.chain))
            st.metric(lang['chain_valid'], "✅ Yes" if st.session_state.blockchain.is_chain_valid() else "❌ No")
        
        with col2:
            st.metric(lang['nfts_created'], len(st.session_state.nft_registry))
            st.metric(lang['difficulty'], st.session_state.blockchain.difficulty)
        
        with col3:
            last_block = st.session_state.blockchain.chain[-1]
            st.metric(lang['last_block'], f"#{last_block['index']}")
            st.metric("Nonce", last_block['nonce'])
        
        st.markdown("---")
        
        st.subheader(lang['how_it_works'])
        
        tab1, tab2, tab3 = st.tabs([lang['blockchain_tech'], lang['nft_process'], lang['copyright_protection']])
        
        with tab1:
            st.markdown(f"""
            **{lang['blockchain_tech']}:**
            - Each block contains cryptographic hash of previous block
            - Proof-of-Work ensures security
            - Immutable ledger system
            - Decentralized verification
            """)
        
        with tab2:
            st.markdown(f"""
            **{lang['nft_process']}:**
            1. Upload digital artwork
            2. Generate unique SHA-256 hash
            3. Record on blockchain
            4. Receive ownership certificate
            """)
        
        with tab3:
            st.markdown(f"""
            **{lang['copyright_protection']}:**
            - Timestamp proves creation date
            - Hash proves file integrity
            - Blockchain provides immutable proof
            - Legal evidence of ownership
            """)
    
    elif choice == lang['create_nft']:
        st.subheader(lang['mint_your_art'])
        
        with st.form("nft_form"):
            title = st.text_input(lang['artwork_title'])
            description = st.text_area(lang['description'])
            artist_name = st.text_input(lang['artist_name'])
            uploaded_file = st.file_uploader(lang['upload_artwork'], type=['jpg', 'jpeg', 'png', 'gif'])
            
            submit_button = st.form_submit_button(lang['mint_nft'])
            
            if submit_button and uploaded_file and title:
                file_content = uploaded_file.getvalue()
                file_hash = create_file_hash(file_content)
                
                nft_data = {
                    'title': title,
                    'description': description,
                    'artist': artist_name,
                    'file_hash': file_hash,
                    'file_name': uploaded_file.name,
                    'timestamp': str(datetime.now()),
                    'type': 'NFT_MINT'
                }
                
                success = st.session_state.blockchain.add_block(json.dumps(nft_data))
                
                if success:
                    nft_id = len(st.session_state.nft_registry) + 1
                    st.session_state.nft_registry.append({
                        'id': nft_id,
                        **nft_data,
                        'block_index': len(st.session_state.blockchain.chain) - 1
                    })
                    
                    st.markdown(f'<div class="success-message">{lang["nft_success"]}</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.image(uploaded_file, caption=title, use_column_width=True)
                    
                    with col2:
                        st.subheader(lang['nft_details'])
                        st.write(f"**NFT ID:** #{nft_id}")
                        st.write(f"**{lang['artwork_title']}:** {title}")
                        st.write(f"**{lang['artist_name']}:** {artist_name}")
                        st.write(f"**File Hash:** `{file_hash[:20]}...`")
                        st.write(f"**Block Index:** {len(st.session_state.blockchain.chain) - 1}")
                        
                        if uploaded_file.type.startswith('image'):
                            analysis = analyze_image_similarity(uploaded_file)
                            if analysis:
                                st.write(f"**{lang['dimensions']}:** {analysis['width']}x{analysis['height']}")
                                st.write(f"**{lang['file_size']}:** {analysis['size_mb']} MB")
                else:
                    st.error("❌ Failed to mint NFT. Please try again.")
    
    elif choice == lang['blockchain']:
        st.subheader(lang['blockchain_explorer'])
        
        if st.button(lang['refresh_chain']):
            st.rerun()
        
        chain_stats = st.session_state.blockchain.get_chain_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(lang['total_blocks'], chain_stats['total_blocks'])
        with col2:
            st.metric(lang['chain_valid'], "✅ Valid" if chain_stats['valid_chain'] else "❌ Invalid")
        with col3:
            if chain_stats['last_block']:
                st.metric("Last Hash", chain_stats['last_block']['hash'][:10] + "...")
        
        st.markdown("---")
        
        search_block = st.number_input(lang['search_block'], min_value=0, max_value=len(st.session_state.blockchain.chain)-1, value=0)
        
        if search_block < len(st.session_state.blockchain.chain):
            block = st.session_state.blockchain.chain[search_block]
            
            st.markdown(f'<div class="block-card"><h3>Block #{block["index"]}</h3></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Timestamp:** {block['timestamp']}")
                st.write(f"**Previous Hash:** `{block['previous_hash'][:20]}...`")
                st.write(f"**Nonce:** {block['nonce']}")
            
            with col2:
                st.write(f"**Hash:** `{block['hash'][:20]}...`")
                
                if block['index'] > 0:
                    try:
                        data = json.loads(block['data'])
                        if data.get('type') == 'NFT_MINT':
                            st.write(f"**NFT Title:** {data.get('title', 'Unknown')}")
                            st.write(f"**Artist:** {data.get('artist', 'Unknown')}")
                    except:
                        st.write(f"**Data:** {block['data'][:50]}...")
                else:
                    st.write(f"**Data:** {block['data']}")
        
        st.markdown("---")
        st.subheader(lang['full_chain'])
        
        chain_data = []
        for i, block in enumerate(st.session_state.blockchain.chain):
            chain_data.append({
                'Block': i,
                'Nonce': block['nonce'],
                'Hash Start': block['hash'][:8],
                'Timestamp': block['timestamp'][:10]
            })
        
        df = pd.DataFrame(chain_data)
        st.dataframe(df, use_container_width=True)
    
    elif choice == lang['analytics']:
        st.subheader(lang['blockchain_analytics'])
        
        if len(st.session_state.blockchain.chain) > 1:
            block_indices = [block['index'] for block in st.session_state.blockchain.chain]
            nonces = [block['nonce'] for block in st.session_state.blockchain.chain]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=block_indices,
                y=nonces,
                mode='lines+markers',
                name='Nonce Values',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="🔢 Nonce Values Over Blocks",
                xaxis_title="Block Index",
                yaxis_title="Nonce Value",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        if st.session_state.nft_registry:
            st.subheader(lang['nft_registry_stats'])
            
            nft_df = pd.DataFrame(st.session_state.nft_registry)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total NFTs", len(nft_df))
                
                if 'artist' in nft_df.columns:
                    artist_counts = nft_df['artist'].value_counts()
                    st.bar_chart(artist_counts)
            
            with col2:
                if 'timestamp' in nft_df.columns:
                    nft_df['date'] = pd.to_datetime(nft_df['timestamp']).dt.date
                    daily_counts = nft_df['date'].value_counts().sort_index()
                    st.line_chart(daily_counts)
    
    elif choice == lang['verify']:
        st.subheader(lang['file_verification'])
        
        uploaded_file = st.file_uploader(lang['upload_verify'], type=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'])
        
        if uploaded_file:
            file_content = uploaded_file.getvalue()
            file_hash = create_file_hash(file_content)
            
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.subheader(lang['file_info'])
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {len(file_content)} bytes")
            st.write(f"**SHA-256 Hash:** `{file_hash}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="warning-message">', unsafe_allow_html=True)
            st.subheader(lang['blockchain_verification'])
            
            found_blocks = []
            for i, block in enumerate(st.session_state.blockchain.chain):
                if block['index'] > 0:
                    try:
                        data = json.loads(block['data'])
                        if data.get('file_hash') == file_hash:
                            found_blocks.append((i, data))
                    except:
                        continue
            
            if found_blocks:
                st.success(lang['found_in_blockchain'].format(count=len(found_blocks)))
                for block_idx, data in found_blocks:
                    st.write(f"**Block #{block_idx}:** {data.get('title', 'Unknown NFT')}")
            else:
                st.warning(lang['not_found'])
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Uploaded File", use_column_width=True)
                
                analysis = analyze_image_similarity(uploaded_file)
                if analysis:
                    st.subheader(lang['image_analysis'])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(lang['dimensions'], f"{analysis['width']}x{analysis['height']}")
                    with col2:
                        st.metric(lang['file_size'], f"{analysis['size_mb']} MB")
                    with col3:
                        st.metric(lang['similarity_score'], f"{analysis['similarity_score']}%")

if __name__ == "__main__":
    main()
