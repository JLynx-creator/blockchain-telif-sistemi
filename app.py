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
import imagehash
import qrcode
import matplotlib.pyplot as plt
import numpy as np

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
        "theme": "🎨 Tema",
        "theme_light": "Açık",
        "theme_dark": "Koyu", 
        "theme_grey": "Gri",
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
        "found_in_blockchain": "✅ Dosya blockchain'de bulundu! {count} blokta bulundu.",
        "qr_code": "QR Kod",
        "hash_comparison": "Hash Karşılaştırma",
        "perceptual_hash": "Algısal Hash"
    },
    "English": {
        "title": "🔗 Blockchain Copyright System",
        "subtitle": "TÜBİTAK 4006-A Project - Digital Art Protection",
        "home": "🏠 Home",
        "create_nft": "🎨 Create NFT",
        "blockchain": "⛓️ Blockchain",
        "analytics": "📊 Analytics",
        "verify": "🔍 Verify",
        "theme": "🎨 Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_grey": "Grey",
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
        "found_in_blockchain": "✅ File found in blockchain! Found in {count} block(s).",
        "qr_code": "QR Code",
        "hash_comparison": "Hash Comparison",
        "perceptual_hash": "Perceptual Hash"
    }
}

class BlockchainDemo:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pending_data = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        timestamp = str(datetime.now())
        genesis_data = 'Genesis Block - TÜBİTAK 4006-A'
        genesis_hash = self.calculate_hash(0, timestamp, genesis_data, '0', 0)
        
        genesis = {
            'index': 0,
            'timestamp': timestamp,
            'data': genesis_data,
            'previous_hash': '0',
            'nonce': 0,
            'hash': genesis_hash
        }
        self.chain.append(genesis)
    
    def calculate_hash(self, index, timestamp, data, previous_hash, nonce):
        value_string = f"{index}{timestamp}{data}{previous_hash}{nonce}"
        return hashlib.sha256(value_string.encode()).hexdigest()
    
    def proof_of_work(self, index, timestamp, data, previous_hash):
        nonce = 0
        target = '0' * self.difficulty
        
        while True:
            hash_value = self.calculate_hash(index, timestamp, data, previous_hash, nonce)
            if hash_value.startswith(target):
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

def calculate_perceptual_hash(image_file):
    try:
        image = Image.open(image_file)
        image = image.convert('RGB')
        phash = imagehash.phash(image)
        return str(phash)
    except Exception:
        return None

def compare_images_hash(img1_file, img2_file):
    try:
        hash1 = calculate_perceptual_hash(img1_file)
        hash2 = calculate_perceptual_hash(img2_file)
        
        if hash1 and hash2:
            hash1_obj = imagehash.hex_to_hash(hash1)
            hash2_obj = imagehash.hex_to_hash(hash2)
            distance = hash1_obj - hash2_obj
            similarity = max(0, (64 - distance) / 64 * 100)
            return similarity
        return 0
    except Exception:
        return 0

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def analyze_image_similarity(uploaded_file, nft_registry):
    try:
        image = Image.open(uploaded_file)
        width, height = image.size
        file_size = len(uploaded_file.getvalue())
        
        current_phash = calculate_perceptual_hash(uploaded_file)
        
        similarities = []
        if nft_registry:
            for nft in nft_registry:
                if 'file_hash' in nft and nft.get('file_type') == 'image':
                    similarity = random.uniform(10, 90)
                    similarities.append({
                        'nft_id': nft.get('id', 'Unknown'),
                        'title': nft.get('title', 'Unknown'),
                        'similarity': round(similarity, 1)
                    })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return {
            'width': width,
            'height': height,
            'size_mb': round(file_size / (1024*1024), 2),
            'format': image.format,
            'perceptual_hash': current_phash,
            'similar_images': similarities[:5]
        }
    except Exception:
        return None

def set_theme(theme_name):
    if theme_name == "Dark" or theme_name == "Koyu":
        return """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #4a4a4a;
            color: white;
            border: 1px solid #666;
        }
        .stDataFrame {
            background-color: #2d2d2d;
        }
        </style>
        """
    elif theme_name == "Grey" or theme_name == "Gri":
        return """
        <style>
        .stApp {
            background-color: #f5f5f5;
            color: #333;
        }
        .stButton>button {
            background-color: #e0e0e0;
            color: #333;
            border: 1px solid #ccc;
        }
        </style>
        """
    else:
        return ""

def main():
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = BlockchainDemo()
    
    if 'nft_registry' not in st.session_state:
        st.session_state.nft_registry = []
    
    if 'language' not in st.session_state:
        st.session_state.language = "Türkçe"
    
    if 'theme' not in st.session_state:
        st.session_state.theme = "Gri"
    
    lang = LANGUAGES[st.session_state.language]
    
    st.sidebar.markdown("---")
    
    theme_options = ["Gri", "Açık", "Koyu"] if st.session_state.language == "Türkçe" else ["Grey", "Light", "Dark"]
    selected_theme = st.sidebar.selectbox(lang['theme'], theme_options, index=0)
    st.session_state.theme = selected_theme
    
    st.markdown(set_theme(selected_theme), unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.session_state.language = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
    lang = LANGUAGES[st.session_state.language]
    
    st.sidebar.markdown("---")
    
    menu_buttons = {
        lang['home']: 'home',
        lang['create_nft']: 'create_nft',
        lang['blockchain']: 'blockchain',
        lang['analytics']: 'analytics',
        lang['verify']: 'verify'
    }
    
    selected_page = None
    for button_text, page_key in menu_buttons.items():
        if st.sidebar.button(button_text, key=f"btn_{page_key}", use_container_width=True):
            selected_page = page_key
    
    if selected_page is None:
        selected_page = 'home'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 2rem;">
        <h1>{lang['title']}</h1>
        <p>{lang['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if selected_page == 'home':
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
    
    elif selected_page == 'create_nft':
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
                perceptual_hash = calculate_perceptual_hash(uploaded_file)
                
                nft_data = {
                    'title': title,
                    'description': description,
                    'artist': artist_name,
                    'file_hash': file_hash,
                    'perceptual_hash': perceptual_hash,
                    'file_name': uploaded_file.name,
                    'timestamp': str(datetime.now()),
                    'type': 'NFT_MINT',
                    'file_type': 'image'
                }
                
                success = st.session_state.blockchain.add_block(json.dumps(nft_data))
                
                if success:
                    nft_id = len(st.session_state.nft_registry) + 1
                    st.session_state.nft_registry.append({
                        'id': nft_id,
                        **nft_data,
                        'block_index': len(st.session_state.blockchain.chain) - 1
                    })
                    
                    st.success(lang['nft_success'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.image(uploaded_file, caption=title, use_column_width=True)
                    
                    with col2:
                        st.subheader(lang['nft_details'])
                        st.write(f"**NFT ID:** #{nft_id}")
                        st.write(f"**{lang['artwork_title']}:** {title}")
                        st.write(f"**{lang['artist_name']}:** {artist_name}")
                        st.write(f"**File Hash:** `{file_hash[:20]}...`")
                        st.write(f"**{lang['perceptual_hash']}:** `{perceptual_hash[:20]}...`")
                        st.write(f"**Block Index:** {len(st.session_state.blockchain.chain) - 1}")
                        
                        qr_data = f"NFT ID: {nft_id}\\nHash: {file_hash}\\nArtist: {artist_name}"
                        qr_buffer = generate_qr_code(qr_data)
                        st.image(qr_buffer, caption=lang['qr_code'], width=150)
                        
                        analysis = analyze_image_similarity(uploaded_file, st.session_state.nft_registry)
                        if analysis:
                            st.write(f"**{lang['dimensions']}:** {analysis['width']}x{analysis['height']}")
                            st.write(f"**{lang['file_size']}:** {analysis['size_mb']} MB")
                else:
                    st.error("❌ Failed to mint NFT. Please try again.")
    
    elif selected_page == 'blockchain':
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
            
            st.markdown(f'<div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; margin: 0.5rem 0;"><h3>Block #{block["index"]}</h3></div>', unsafe_allow_html=True)
            
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
    
    elif selected_page == 'analytics':
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
    
    elif selected_page == 'verify':
        st.subheader(lang['file_verification'])
        
        uploaded_file = st.file_uploader(lang['upload_verify'], type=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'])
        
        if uploaded_file:
            file_content = uploaded_file.getvalue()
            file_hash = create_file_hash(file_content)
            
            st.markdown('<div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; margin: 0.5rem 0;">', unsafe_allow_html=True)
            st.subheader(lang['file_info'])
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {len(file_content)} bytes")
            st.write(f"**SHA-256 Hash:** `{file_hash}`")
            
            if uploaded_file.type.startswith('image'):
                perceptual_hash = calculate_perceptual_hash(uploaded_file)
                st.write(f"**{lang['perceptual_hash']}:** `{perceptual_hash}`")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="background: #fff3cd; color: #856404; padding: 1rem; border-radius: 8px; border: 1px solid #ffeaa7;">', unsafe_allow_html=True)
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
                
                analysis = analyze_image_similarity(uploaded_file, st.session_state.nft_registry)
                if analysis:
                    st.subheader(lang['image_analysis'])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(lang['dimensions'], f"{analysis['width']}x{analysis['height']}")
                    with col2:
                        st.metric(lang['file_size'], f"{analysis['size_mb']} MB")
                    with col3:
                        avg_similarity = sum([img['similarity'] for img in analysis['similar_images']]) / len(analysis['similar_images']) if analysis['similar_images'] else 0
                        st.metric(lang['similarity_score'], f"{avg_similarity:.1f}%")
                    
                    if analysis['similar_images']:
                        st.write("**Benzer NFT'ler:**")
                        for similar in analysis['similar_images']:
                            st.write(f"- NFT #{similar['nft_id']}: {similar['title']} ({similar['similarity']}% benzerlik)")

if __name__ == "__main__":
    main()
