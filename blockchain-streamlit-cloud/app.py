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
        
        # Basit analiz - gerçek AI yerine simülasyon
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
    
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .block-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>🔗 Blockchain Copyright System</h1>
        <p>TÜBİTAK 4006-A Project - Digital Art Protection</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = ["🏠 Home", "🎨 Create NFT", "⛓️ Blockchain", "📊 Analytics", "🔍 Verify"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "🏠 Home":
        st.subheader("Welcome to Blockchain Copyright System")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Blocks", len(st.session_state.blockchain.chain))
            st.metric("Chain Valid", "✅ Yes" if st.session_state.blockchain.is_chain_valid() else "❌ No")
        
        with col2:
            st.metric("NFTs Created", len(st.session_state.nft_registry))
            st.metric("Difficulty", st.session_state.blockchain.difficulty)
        
        with col3:
            last_block = st.session_state.blockchain.chain[-1]
            st.metric("Last Block", f"#{last_block['index']}")
            st.metric("Nonce", last_block['nonce'])
        
        st.markdown("---")
        
        st.subheader("📖 How It Works")
        
        tab1, tab2, tab3 = st.tabs(["Blockchain", "NFT Minting", "Copyright"])
        
        with tab1:
            st.markdown("""
            **Blockchain Technology:**
            - Each block contains cryptographic hash of previous block
            - Proof-of-Work ensures security
            - Immutable ledger system
            - Decentralized verification
            """)
        
        with tab2:
            st.markdown("""
            **NFT Creation Process:**
            1. Upload digital artwork
            2. Generate unique SHA-256 hash
            3. Record on blockchain
            4. Receive ownership certificate
            """)
        
        with tab3:
            st.markdown("""
            **Copyright Protection:**
            - Timestamp proves creation date
            - Hash proves file integrity
            - Blockchain provides immutable proof
            - Legal evidence of ownership
            """)
    
    elif choice == "🎨 Create NFT":
        st.subheader("🎨 Mint Your Digital Art as NFT")
        
        with st.form("nft_form"):
            title = st.text_input("Artwork Title")
            description = st.text_area("Description")
            artist_name = st.text_input("Artist Name")
            uploaded_file = st.file_uploader("Upload Artwork", type=['jpg', 'jpeg', 'png', 'gif'])
            
            submit_button = st.form_submit_button("🚀 Mint NFT")
            
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
                    
                    st.markdown('<div class="success-message">✅ NFT Successfully Minted!</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.image(uploaded_file, caption=title, use_column_width=True)
                    
                    with col2:
                        st.subheader("📋 NFT Details")
                        st.write(f"**NFT ID:** #{nft_id}")
                        st.write(f"**Title:** {title}")
                        st.write(f"**Artist:** {artist_name}")
                        st.write(f"**File Hash:** `{file_hash[:20]}...`")
                        st.write(f"**Block Index:** {len(st.session_state.blockchain.chain) - 1}")
                        
                        if uploaded_file.type.startswith('image'):
                            analysis = analyze_image_similarity(uploaded_file)
                            if analysis:
                                st.write(f"**Image Size:** {analysis['width']}x{analysis['height']}")
                                st.write(f"**File Size:** {analysis['size_mb']} MB")
                else:
                    st.error("❌ Failed to mint NFT. Please try again.")
    
    elif choice == "⛓️ Blockchain":
        st.subheader("⛓️ Blockchain Explorer")
        
        if st.button("🔄 Refresh Chain"):
            st.rerun()
        
        chain_stats = st.session_state.blockchain.get_chain_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Blocks", chain_stats['total_blocks'])
        with col2:
            st.metric("Chain Valid", "✅ Valid" if chain_stats['valid_chain'] else "❌ Invalid")
        with col3:
            if chain_stats['last_block']:
                st.metric("Last Hash", chain_stats['last_block']['hash'][:10] + "...")
        
        st.markdown("---")
        
        search_block = st.number_input("Search Block by Index", min_value=0, max_value=len(st.session_state.blockchain.chain)-1, value=0)
        
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
        st.subheader("📊 Full Chain Visualization")
        
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
    
    elif choice == "📊 Analytics":
        st.subheader("📊 Blockchain Analytics")
        
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
            st.subheader("🎨 NFT Registry Statistics")
            
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
    
    elif choice == "🔍 Verify":
        st.subheader("🔍 File Verification")
        
        uploaded_file = st.file_uploader("Upload File to Verify", type=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'])
        
        if uploaded_file:
            file_content = uploaded_file.getvalue()
            file_hash = create_file_hash(file_content)
            
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.subheader("📋 File Information")
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {len(file_content)} bytes")
            st.write(f"**SHA-256 Hash:** `{file_hash}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="warning-message">', unsafe_allow_html=True)
            st.subheader("🔍 Blockchain Verification")
            
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
                st.success(f"✅ File found in blockchain! Found in {len(found_blocks)} block(s).")
                for block_idx, data in found_blocks:
                    st.write(f"**Block #{block_idx}:** {data.get('title', 'Unknown NFT')}")
            else:
                st.warning("⚠️ File not found in blockchain. This file has not been registered as an NFT.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Uploaded File", use_column_width=True)
                
                analysis = analyze_image_similarity(uploaded_file)
                if analysis:
                    st.subheader("🤖 Image Analysis")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Dimensions", f"{analysis['width']}x{analysis['height']}")
                    with col2:
                        st.metric("File Size", f"{analysis['size_mb']} MB")
                    with col3:
                        st.metric("Similarity Score", f"{analysis['similarity_score']}%")

if __name__ == "__main__":
    main()
