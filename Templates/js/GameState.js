let socket;

let gameState = null;
let selectedHandIndex = null;
let sortMenuOpen = false;

document.addEventListener("DOMContentLoaded", () => {
    init();
});

function init() {
    socket = io();

    setupSocketListeners();
    setupUIListeners();
    createActionBar();
    createSortMenu();

    socket.emit("join_game");
}

function setupSocketListeners() {
    socket.on("connect", () => {
        socket.emit("join_game");
    });

    socket.on("game_state", (data) => {
        if (!data || !data.success) {
            return;
        }

        gameState = data.state || null;
        selectedHandIndex = null;

        renderGameState();
        handleWinner();
    });

    socket.on("game_started", () => {
        window.location.href = "/GameState";
    });

    socket.on("game_paused", (data) => {
        showPausedOverlay(data?.message || "A player disconnected. The game was paused.");
    });

    socket.on("message", (data) => {
        if (data?.message) {
            console.log(data.message);
        }
    });

    socket.on("error", (data) => {
        if (data?.error) {
            alert(data.error);
        }
    });
}

function setupUIListeners() {
    const deckPile = document.getElementById("deck-pile");
    const discardPile = document.getElementById("discard-pile");
    const sortButton = document.getElementById("sort-hand-button");
    const helpClose = document.getElementById("help-close");

    if (deckPile) {
        deckPile.addEventListener("click", onDeckClick);
    }

    if (discardPile) {
        discardPile.addEventListener("click", onDiscardPileClick);
    }

    if (sortButton) {
        sortButton.addEventListener("click", toggleSortMenu);
    }

    if (helpClose) {
        helpClose.addEventListener("click", closeHelpModal);
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            toggleHelpModal();
        }
    });
}

function renderGameState() {
    if (!gameState) {
        return;
    }

    hidePausedOverlay();
    renderStatusChip();
    renderCenterPiles();
    renderTableMelds();
    renderPlayerHand();
    renderOpponents();
    renderCurrentPlayerLabel();
    renderHelpModalContent();
    updateActionButtons();
}

function renderStatusChip() {
    const statusText = document.getElementById("table-status-text");
    if (!statusText || !gameState) {
        return;
    }

    if (isMyTurn()) {
        if (!gameState.has_drawn) {
            statusText.textContent = "Your turn: draw from the deck or discard pile.";
            return;
        }

        if (getSelectedHandCard()) {
            statusText.textContent = "Card selected: choose SELECT, DISCARD, or click a meld to lay off.";
            return;
        }

        if (hasStoredCards()) {
            statusText.textContent = "Stored cards available: use STORE MELD or MELD, or select a card to discard.";
            return;
        }

        statusText.textContent = "Your turn: build melds or choose a card to discard.";
        return;
    }

    const currentPlayer = getCurrentTurnPlayer();
    statusText.textContent = currentPlayer
        ? `Waiting for ${currentPlayer.username} to take their turn.`
        : "Waiting for another player.";
}

function renderCenterPiles() {
    const deckPile = document.getElementById("deck-pile");
    const discardPile = document.getElementById("discard-pile");

    if (deckPile) {
        setCardBack(deckPile);
        deckPile.textContent = String(gameState.deck_size ?? "");
        deckPile.title = "Draw a hidden card from the deck";
    }

    if (discardPile) {
        discardPile.textContent = "";

        if (gameState.discard_top) {
            setCardFace(discardPile, gameState.discard_top);
            discardPile.title = "Draw the visible top card from the discard pile";
        } else {
            setCardBack(discardPile);
            discardPile.title = "Discard pile";
        }
    }
}

function renderTableMelds() {
    const meldArea = document.getElementById("meld-area");
    if (!meldArea) {
        return;
    }

    meldArea.innerHTML = "";

    const melds = Array.isArray(gameState.table_melds) ? gameState.table_melds : [];
    const canLayOff = isMyTurn() && !!getSelectedHandCard();

    melds.forEach((meld, meldIndex) => {
        const row = document.createElement("div");
        row.className = "meld-row";

        if (canLayOff) {
            row.classList.add("layoff-target");
        }

        row.addEventListener("click", () => onMeldClick(meldIndex));

        meld.forEach((card) => {
            const cardEl = document.createElement("button");
            cardEl.type = "button";
            cardEl.className = "card table-card";
            setCardFace(cardEl, card);
            cardEl.setAttribute("aria-label", `${card.rank} of ${card.suit}`);
            row.appendChild(cardEl);
        });

        meldArea.appendChild(row);
    });
}

function renderPlayerHand() {
    const handEl = document.getElementById("player-hand");
    if (!handEl) {
        return;
    }

    handEl.innerHTML = "";
    handEl.classList.toggle("your-turn", isMyTurn());
    handEl.classList.toggle("not-your-turn", !isMyTurn());

    const hand = Array.isArray(gameState.hand) ? gameState.hand : [];
    const selectedCards = Array.isArray(gameState.selected_cards) ? gameState.selected_cards : [];
    const count = hand.length;

    if (count === 0) {
        return;
    }

    const spread = Math.min(70, 800 / Math.max(count, 1));
    const totalWidth = spread * Math.max(count - 1, 0);
    const startX = (980 - 120 - totalWidth) / 2;

    hand.forEach((card, index) => {
        const cardEl = document.createElement("button");
        cardEl.type = "button";
        cardEl.className = "card hand-card";

        const x = startX + index * spread;
        const rotation = (index - (count - 1) / 2) * 4;
        const y = Math.abs(index - (count - 1) / 2) * 4;

        cardEl.style.left = `${x}px`;
        cardEl.style.bottom = `${y}px`;
        cardEl.style.transform = `rotate(${rotation}deg)`;

        if (selectedHandIndex === index) {
            cardEl.style.bottom = `${y + 30}px`;
        }

        if (isCardInList(card, selectedCards)) {
            cardEl.classList.add("selected-card-outline");
        }

        setCardFace(cardEl, card);
        cardEl.setAttribute("aria-label", `${card.rank} of ${card.suit}`);
        cardEl.addEventListener("click", () => onHandCardClick(index));

        handEl.appendChild(cardEl);
    });
}

function renderOpponents() {
    const layer = document.getElementById("opponents-layer");
    if (!layer) {
        return;
    }

    layer.innerHTML = "";

    const currentUserId = getCurrentUserId();
    const players = Array.isArray(gameState.players) ? gameState.players : [];
    const opponents = players.filter((player) => Number(player.player_id) !== currentUserId);

    const positions = [
        { left: "18%", top: "28%" },
        { left: "50%", top: "8%" },
        { left: "82%", top: "28%" }
    ];

    opponents.forEach((opponent, index) => {
        const seat = document.createElement("div");
        seat.className = "opponent-seat";

        const pos = positions[index] || positions[positions.length - 1];
        seat.style.left = pos.left;
        seat.style.top = pos.top;

        const label = document.createElement("div");
        label.className = "opponent-label";
        label.textContent = `${opponent.username} (${opponent.hand_size})`;

        if (Number(opponent.player_id) === Number(gameState.curent_player)) {
            label.classList.add("turn-highlight");
        }

        const fan = document.createElement("div");
        fan.className = "opponent-fan";

        const visibleCards = Math.min(opponent.hand_size || 0, 12);

        for (let i = 0; i < visibleCards; i++) {
            const cardEl = document.createElement("div");
            cardEl.className = "card opponent-card";

            const offset = (i - (visibleCards - 1) / 2) * 18;
            const rotation = (i - (visibleCards - 1) / 2) * 7;

            cardEl.style.left = `${offset}px`;
            cardEl.style.top = "0px";
            cardEl.style.transform = `translateX(-50%) rotate(${rotation}deg)`;

            setCardBack(cardEl);
            fan.appendChild(cardEl);
        }

        seat.appendChild(label);
        seat.appendChild(fan);
        layer.appendChild(seat);
    });
}

function renderCurrentPlayerLabel() {
    const label = document.getElementById("current-player-label");
    if (!label) {
        return;
    }

    const me = getMe();
    label.textContent = me ? me.username : "Player";
    label.classList.toggle("active-turn", isMyTurn());
}

function createActionBar() {
    const bar = document.getElementById("hand-action-bar");
    if (!bar || bar.children.length > 0) {
        return;
    }

    const selectButton = createActionButton("select-card-button", "SELECT", onSelectCard);
    const discardButton = createActionButton("discard-card-button", "DISCARD", onDiscardCard);
    const storeMeldButton = createActionButton("store-meld-button", "STORE MELD", onStoreMeld);
    const meldButton = createActionButton("meld-button", "MELD", onMeld);
    const clearButton = createActionButton("clear-selection-button", "CLEAR", onDeselectAll);

    bar.appendChild(selectButton);
    bar.appendChild(discardButton);
    bar.appendChild(storeMeldButton);
    bar.appendChild(meldButton);
    bar.appendChild(clearButton);
}

function createActionButton(id, text, handler) {
    const button = document.createElement("button");
    button.type = "button";
    button.id = id;
    button.className = "box button small-button";
    button.textContent = text;
    button.addEventListener("click", handler);
    return button;
}

function updateActionButtons() {
    const selectButton = document.getElementById("select-card-button");
    const discardButton = document.getElementById("discard-card-button");
    const storeMeldButton = document.getElementById("store-meld-button");
    const meldButton = document.getElementById("meld-button");
    const clearButton = document.getElementById("clear-selection-button");

    const selectedCard = getSelectedHandCard();
    const myTurn = isMyTurn();
    const hasSelectedCards = hasStoredCards();

    if (selectButton) {
        selectButton.disabled = !(myTurn && selectedCard);
        selectButton.title = selectedCard ? "Store the selected card for meld building" : "Select a card first";
    }

    if (discardButton) {
        discardButton.disabled = !(myTurn && selectedCard && gameState?.has_drawn);
        discardButton.title = gameState?.has_drawn
            ? "Discard the selected card and end your turn"
            : "You must draw before discarding";
    }

    if (storeMeldButton) {
        storeMeldButton.disabled = !(myTurn && hasSelectedCards);
        storeMeldButton.title = hasSelectedCards
            ? "Group selected stored cards into a stored meld"
            : "Select and store cards first";
    }

    if (meldButton) {
        meldButton.disabled = !myTurn;
        meldButton.title = "Play your stored melds to the table";
    }

    if (clearButton) {
        clearButton.disabled = !(myTurn && hasSelectedCards);
        clearButton.title = hasSelectedCards
            ? "Clear all currently stored selected cards"
            : "No stored selected cards to clear";
    }
}

function onDeckClick() {
    if (!gameState || !isMyTurn() || gameState.has_drawn) {
        return;
    }

    emitMove("Draw_Deck");
}

function onDiscardPileClick() {
    if (!gameState || !isMyTurn() || gameState.has_drawn) {
        return;
    }

    emitMove("Draw_Discard");
}

function onHandCardClick(index) {
    if (!gameState || !isMyTurn()) {
        return;
    }

    const hand = Array.isArray(gameState.hand) ? gameState.hand : [];
    if (!hand[index]) {
        return;
    }

    selectedHandIndex = selectedHandIndex === index ? null : index;

    renderPlayerHand();
    renderTableMelds();
    updateActionButtons();
}

function onMeldClick(meldIndex) {
    if (!gameState || !isMyTurn()) {
        return;
    }

    const card = getSelectedHandCard();
    if (!card) {
        return;
    }

    emitMove("Lay_Off", {
        card: card,
        meld_index: meldIndex
    });
}

function onSelectCard() {
    const card = getSelectedHandCard();
    if (!card || !isMyTurn()) {
        return;
    }

    emitMove("Store_Card", { card: card });
}

function onDiscardCard() {
    const card = getSelectedHandCard();
    if (!card || !isMyTurn()) {
        return;
    }

    emitMove("Discard", { card: card });
}

function onStoreMeld() {
    if (!isMyTurn()) {
        return;
    }

    emitMove("Store_Meld");
}

function onMeld() {
    if (!isMyTurn()) {
        return;
    }

    emitMove("Meld");
}

function onDeselectAll() {
    if (!isMyTurn()) {
        return;
    }

    selectedHandIndex = null;
    emitMove("Deselect_all");
    renderPlayerHand();
    renderTableMelds();
    updateActionButtons();
}

function getSelectedHandCard() {
    if (!gameState || selectedHandIndex === null) {
        return null;
    }

    const hand = Array.isArray(gameState.hand) ? gameState.hand : [];
    return hand[selectedHandIndex] || null;
}

function hasStoredCards() {
    return Array.isArray(gameState?.selected_cards) && gameState.selected_cards.length > 0;
}

function createSortMenu() {
    const sortButton = document.getElementById("sort-hand-button");
    if (!sortButton || document.getElementById("sort-menu")) {
        return;
    }

    const menu = document.createElement("div");
    menu.id = "sort-menu";
    menu.className = "box";
    menu.style.position = "absolute";
    menu.style.right = "0";
    menu.style.bottom = "80px";
    menu.style.display = "none";
    menu.style.flexDirection = "column";
    menu.style.zIndex = "20";

    const rankButton = document.createElement("button");
    rankButton.type = "button";
    rankButton.className = "box button small-button";
    rankButton.textContent = "Rank";
    rankButton.addEventListener("click", () => onSortChoice("Sort_Rank"));

    const suitButton = document.createElement("button");
    suitButton.type = "button";
    suitButton.className = "box button small-button";
    suitButton.textContent = "Suit";
    suitButton.addEventListener("click", () => onSortChoice("Sort_Suit"));

    menu.appendChild(rankButton);
    menu.appendChild(suitButton);

    sortButton.parentElement.style.position = "relative";
    sortButton.parentElement.appendChild(menu);
}

function toggleSortMenu() {
    const menu = document.getElementById("sort-menu");
    if (!menu) {
        return;
    }

    sortMenuOpen = !sortMenuOpen;
    menu.style.display = sortMenuOpen ? "flex" : "none";
}

function onSortChoice(moveType) {
    sortMenuOpen = false;

    const menu = document.getElementById("sort-menu");
    if (menu) {
        menu.style.display = "none";
    }

    if (!isMyTurn()) {
        return;
    }

    emitMove(moveType);
}

function toggleHelpModal() {
    const modal = document.getElementById("help-modal");
    if (!modal) {
        return;
    }

    if (modal.classList.contains("active")) {
        closeHelpModal();
    } else {
        openHelpModal();
    }
}

function openHelpModal() {
    const modal = document.getElementById("help-modal");
    if (!modal) {
        return;
    }

    renderHelpModalContent();
    modal.classList.add("active");
}

function closeHelpModal() {
    const modal = document.getElementById("help-modal");
    if (!modal) {
        return;
    }

    modal.classList.remove("active");
}

function renderHelpModalContent() {
    const container = document.getElementById("help-content");
    if (!container || !gameState) {
        return;
    }

    const rules = getReadableRules();

    container.innerHTML = `
        <div class="box help-section">
            <div class="help-section-title">Turn Order</div>
            <div class="help-line">1. Draw from the <span class="help-key">deck</span> or <span class="help-key">discard pile</span>.</div>
            <div class="help-line">2. Click cards in your hand to choose them.</div>
            <div class="help-line">3. Press <span class="help-key">SELECT</span> to store chosen cards.</div>
            <div class="help-line">4. Press <span class="help-key">STORE MELD</span> to group selected cards into a stored meld.</div>
            <div class="help-line">5. Press <span class="help-key">MELD</span> to play stored melds onto the table.</div>
            <div class="help-line">6. To lay off, choose a card and click a meld already on the table.</div>
            <div class="help-line">7. Press <span class="help-key">DISCARD</span> on a chosen card to end your turn.</div>
        </div>

        <div class="box help-section">
            <div class="help-section-title">Action Buttons</div>
            <div class="help-line"><span class="help-key">SELECT</span>: stores the chosen card for meld building.</div>
            <div class="help-line"><span class="help-key">STORE MELD</span>: groups currently selected stored cards into a meld.</div>
            <div class="help-line"><span class="help-key">MELD</span>: plays stored melds to the table.</div>
            <div class="help-line"><span class="help-key">DISCARD</span>: discards the chosen card and ends your turn.</div>
            <div class="help-line"><span class="help-key">CLEAR</span>: removes all currently stored selected cards.</div>
            <div class="help-line"><span class="help-key">Sort Hand</span>: sort by rank or suit.</div>
        </div>

        <div class="box help-section">
            <div class="help-section-title">Current Rules</div>
            ${rules.map((rule) => `<div class="help-line">${rule}</div>`).join("")}
        </div>
    `;
}

function getReadableRules() {
    const rules = gameState?.rules || {};

    return [
        `Sets allowed: ${readableBool(rules.allow_sets)}`,
        `Runs allowed: ${readableBool(rules.allow_runs)}`,
        `Minimum meld size: ${readableValue(rules.min_meld_size)}`,
        `Maximum set size: ${readableValue(rules.max_meld_size_set)}`,
        `Maximum run size: ${readableValue(rules.max_meld_size_run)}`,
        `Required initial meld score: ${readableValue(gameState.required_meld_score)}`,
        `Initial hand size: ${readableValue(rules.initial_hand_size)}`,
        `Number of decks: ${readableValue(rules.num_decks)}`,
        `Ace high: ${readableBool(rules.ace_high)}`,
        `Ace low: ${readableBool(rules.ace_low)}`,
        `Ace both: ${readableBool(rules.ace_both)}`,
        `Wild replacement allowed: ${readableBool(rules.allow_wild_replacement)}`,
        `Wild-only melds allowed: ${readableBool(rules.allow_wild_only_melds)}`,
        `Require melding before lay off: ${readableBool(rules.require_melding_to_lay_off)}`,
        `Winner deadwood score: ${readableValue(rules.winner_deadwood)}`
    ];
}

function readableBool(value) {
    if (value === true) return "Yes";
    if (value === false) return "No";
    return "Unknown";
}

function readableValue(value) {
    return value ?? "Unknown";
}

function emitMove(moveType, extraData = {}) {
    socket.emit("apply_move", {
        move_type: moveType,
        ...extraData
    });
}

function isMyTurn() {
    if (!gameState) {
        return false;
    }

    return Number(gameState.curent_player) === getCurrentUserId();
}

function getCurrentTurnPlayer() {
    return (gameState?.players || []).find(
        (player) => Number(player.player_id) === Number(gameState.curent_player)
    ) || null;
}

function getMe() {
    return (gameState?.players || []).find(
        (player) => Number(player.player_id) === getCurrentUserId()
    ) || null;
}

function handleWinner() {
    if (!gameState || !gameState.winner) {
        return;
    }

    const winnerPlayer = (gameState.players || []).find(
        (player) => Number(player.player_id) === Number(gameState.winner)
    );

    const winnerName = winnerPlayer ? winnerPlayer.username : "Unknown";
    alert(`Winner: ${winnerName}`);
    window.location.href = "/";
}

function showPausedOverlay(message) {
    const overlay = document.getElementById("game-paused-overlay");
    const text = document.getElementById("game-paused-text");

    if (text) {
        text.textContent = message;
    }

    if (overlay) {
        overlay.style.display = "flex";
    }

    setTimeout(() => {
        window.location.href = "/";
    }, 1500);
}

function hidePausedOverlay() {
    const overlay = document.getElementById("game-paused-overlay");
    if (overlay) {
        overlay.style.display = "none";
    }
}

function getCurrentUserId() {
    return Number(document.body.dataset.userId);
}

function isCardInList(card, list) {
    return list.some((item) => sameCard(card, item));
}

function sameCard(a, b) {
    if (!a || !b) {
        return false;
    }

    return String(a.rank) === String(b.rank) && String(a.suit) === String(b.suit);
}

function setCardFace(element, card) {
    const filename = getCardFilename(card);
    element.style.backgroundImage = `url("/static/textures/cards/${filename}.png")`;
    element.style.backgroundSize = "cover";
    element.style.backgroundPosition = "center";
    element.style.backgroundRepeat = "no-repeat";
    element.textContent = "";
}

function setCardBack(element) {
    element.style.backgroundImage = 'url("/static/textures/cards/back.png")';
    element.style.backgroundSize = "cover";
    element.style.backgroundPosition = "center";
    element.style.backgroundRepeat = "no-repeat";
}

function getCardFilename(card) {
    const suitLetter = String(card.suit || "").trim().charAt(0).toUpperCase();
    const rankIndex = getRankIndex(card.rank);
    return `${suitLetter}-${rankIndex}`;
}

function getRankIndex(rank) {
    const text = String(rank);

    const map = {
        "Ace": 1,
        "Jack": 11,
        "Queen": 12,
        "King": 13,
        "Joker": 0
    };

    if (map[text] !== undefined) {
        return map[text];
    }

    const numeric = Number(text);
    return Number.isNaN(numeric) ? 0 : numeric;
}