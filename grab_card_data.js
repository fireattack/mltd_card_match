var cards = document.querySelectorAll('.a-card-select');

var cardsData = [];

cards.forEach(card => {
    if (card.parentNode.parentNode.parentNode.id.startsWith('idol-list')) {
        let idolID = card.parentNode.parentNode.parentNode.id.replace('idol-list-', '');
        let cardName = card.textContent.trim();
        let cardID = card.href.match(/\d+/)[0];
        let iconImg1 = card.querySelector('.card-icon').style.backgroundImage.match(/"(.+)"/)[1].replace('_1.p', '_0.p');
        let iconImg2 = card.querySelector('.card-icon').style.backgroundImage.match(/url\("(.+)"/)[1];
        let type1 = card.querySelectorAll('.card-icon-overlay')[0].style.backgroundImage.match(/\/([^/]+?)\./)[1];
        let type2 = card.querySelectorAll('.card-icon-overlay')[1].style.backgroundImage.match(/\/([^/]+?)\./)[1];

        let obj = {
            idolID: idolID,
            cardName: cardName,
            cardID: cardID,
            iconImg1: iconImg1,
            iconImg2: iconImg2,
            type1: type1,
            type2: type2
        };
        cardsData.push(obj);
    }

});

copy(cardsData);