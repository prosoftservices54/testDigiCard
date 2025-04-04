let canSpin = false;
let admin = true;
let prefix = "";
let isLogin = false;
let links = [];
let rewards = [];
let possible_rewards = [];

$(document).ready(function () {
    // Check if user is logged in and if he is an admin
    const loggedInUser = getCookie('loggedInUser');
    if(loggedInUser){
        isLogin = true;
        admin = loggedInUser === "admin";
    } else {
        isLogin = false;
        admin = false;
    }

    if(admin)
        prefix = "admin-";

    // If user is logged in, show some content
    if (isLogin) {
        $("header").removeClass("hidden");
        $('#login-section').addClass("hidden");
        $("#" + prefix + "game-content").removeClass("hidden");
        $("#visitCount").text(getCookie('visits'));
        let rews = [];
        JSON.parse(getCookie('rewards')).forEach(reward => {
            rews.push(reward);
        });
        $("#nb-games").text("Nombre de parties jouables : " + getCookie('games'));
        displayRewards(rews);
        setupLinks();
    } else {
        $('#connexion').removeClass("hidden");
        $("header").addClass("hidden");
    }


    /**
     * Buttons management
     */
    $('#spinButton').on('click', spin);

    $(".button-navbar").click(function() {
        $(".button-navbar.active").toggleClass("active");
        $(this).toggleClass("active");
        $("main > div").addClass("hidden");
        $("#" + prefix + $(this).attr("id") + "-content").removeClass("hidden");
    });

    $('#login-button').on('click', function (e) {
        login($("#phone").val(), $("#password").val());
    });

    function logout(){
        document.cookie = "loggedInUser=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "phone=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "visits=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "rewards=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "links=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "games=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        $('#login-section').removeClass("hidden");
        $("#account-content").addClass("hidden");
        $("header").addClass("hidden");
        $("#" + prefix + "game-content").addClass("hidden");
        location.reload();
    }
    
    $("#logoutButton").on('click', function () {
        logout()
    });

    $("#logoutButtonAdmin").on('click', function () {
        logout()
    })

    $("#register-button").on('click', function () {
        register($("#newPassword").val(), $("#newPhone").val(), $("#newBirthdate").val(), $("#newGender").val());
    });

    $("#register-menu").on('click', function () {
        $("#register-section").removeClass("hidden");
        $("#login-section").addClass("hidden");
    });

    // Display popup
    function showReviewPopup() {
        $('#google-review-popup').removeClass('hidden');
    }

    // Close popup
    function closeReviewPopup() {
        $('#google-review-popup').addClass('hidden');
    }

    // Close popup when clicking on close button
    $('#close-popup').on('click', closeReviewPopup);

    // Close popup when clicking outside
    $(document).on('click', function (event) {
        if ($(event.target).is('#google-review-popup')) {
            closeReviewPopup();
        }
    });

    if(isLogin)
        canSpin = JSON.parse(getCookie('links')).length > 0 && getCookie('games') > 0;

    // Update the wheel state
    if(!canSpin){
        $("#spinButton").addClass("disabled");
        $("#unlock-wheel").removeClass("hidden");
    } else {
        $("#unlock-wheel").text("Partager");
    }

    $("#unlock-wheel").on("click", function () {
        showReviewPopup();
    });

    $("#check-review").on("click", function () {
        canSpin = true;
        $("#spinButton").removeClass("disabled");
        $("#unlock-wheel").addClass("hidden");
        setCookie('games', parseInt(getCookie('games')) + 1, 7);
        $("#nb-games").text("Nombre de parties jouables : " + getCookie('games'));
        validateReview();
        closeReviewPopup();
    });

    // Init links
    if(isLogin){
        getLinks().then(data => {
            links = data.links;
            renderLinks();
        });
        getRewards().then(data => {
            rewards = data.rewards
            renderRewards();
        })
    }

    $("#add-link").on("click", addLink);

    function addLink() {
        links.push({ name: "", link: "" });
        renderLinks();
    }

    $("#add-reward").on("click", addReward);


    function addReward() {
        rewards.push({ reward: ""});
        renderRewards();
    }

    function loadClients() {
        fetch("http://127.0.0.1:5000/customers")
            .then(response => response.json())
            .then(data => displayClients(data.clients))
            .catch(error => console.error(error));
    }

    function displayClients(clients) {

        // Réinitialiser la liste avant d'ajouter des éléments
        const $clientsList = $('#clients-list');
        $clientsList.empty();

        // Ajouter chaque client à la liste
        clients.forEach(client => {
            $clientsList.append(`
                <p>
                    <strong>Téléphone :</strong> ${client.phone}<br>
                    <strong>Nombre de visites :</strong> ${client.visits}<br>
                    <strong>Date de naissance :</strong> ${client.birthDate}<br>
                    <strong>Genre :</strong> ${client.gender}
                    <button class="delete-client" data-phone="${client.phone}">Supprimer</button>
                </p>
                <hr>
            `);
        });
    }

    // Supprimer un client
    $(document).off('click', '.delete-client').on('click', '.delete-client', function () {
        const phone = $(this).data('phone');
        fetch("http://127.0.0.1:5000/customer/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                phone: phone
            })
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Erreur lors de la suppression du client.");
            }
        }).then(data => {
            if (!data.success) {
                throw new Error("Impossible de supprimer le client.");
            }
            loadClients();
        }).catch(error => {
            console.error(error);
        });
    });
    
    // Charger les clients au chargement de la page
    loadClients();

    // Optionnel : Rechercher un client
    $('#phone-input-counter').on('input', function () {
        const searchQuery = $(this).val().toLowerCase();

        $('#clients-list p').each(function () {
            const clientText = $(this).text().toLowerCase();
            $(this).toggle(clientText.includes(searchQuery));
        });
    });

    // Bouton "Ajouter une visite" (exemple)
    $('#search-button').on('click', function () {
        const phone = $('#phone-input-counter').val();
        
        if (!phone) {
            alert('Veuillez entrer un numéro de téléphone avant de continuer.');
            return;
        }

        addVisit(phone);
    });
});

/**
 * Other methods
 */
// Fonction pour afficher les liens
function renderLinks() {
    $("#link-container").empty(); // Vide le conteneur avant de tout recharger
    links.forEach((link, index) => {
        const box = `
            <div class="link-box">
                <input type="text" class="link-name" value="${link.name}" placeholder="Nom du lien" />
                <input type="url" class="link-url" value="${link.link}" placeholder="URL du lien" />
                <button class="save-link" data-index="${index}">Sauvegarder</button>
                <button class="delete-link" data-index="${index}">Supprimer</button>
            </div>
        `;
        $("#link-container").append(box);
    });

    // Check if there is a change in the links
    $(document).off("click", ".save-link").on("click", ".save-link", function () {
        const index = $(this).data("index");
        const name = $(this).siblings(".link-name").val().trim();
        const url = $(this).siblings(".link-url").val().trim();

        if (name === "" || url === "") {
            alert("Veuillez remplir les deux champs.");
            return;
        }

        // Mettre à jour les données
        updateLink(links[index].id, name, url);
    });

    // Écouteur pour supprimer un lien
    $(document).off("click", ".delete-link").on("click", ".delete-link", function () {
        const index = $(this).data("index");
        deleteLink(links[index].id);
        links.splice(index, 1); // Supprimer l'élément correspondant à l'index
        renderLinks(); // Recharger les liens
    });
}

function displayRewards(customer_rewards){
    $("#rewardList").empty();
    customer_rewards.forEach(reward => {
        $("#rewardList").append(`<p>${reward}</p>`);
    });
}

// Fonction pour afficher les liens
function renderRewards() {
    $("#reward-container").empty(); // Vide le conteneur avant de tout recharger
    rewards.forEach((reward, index) => {
        const box = `
            <div class="reward-box">
                <input type="text" class="reward-name" value="${reward.reward}" placeholder="Récompense" />
                <button class="save-reward" data-index="${index}">Sauvegarder</button>
                <button class="delete-reward" data-index="${index}">Supprimer</button>
            </div>
        `;
        $("#reward-container").append(box);
    });

    // Check if there is a change in the links
    $(document).off("click", ".save-reward").on("click", ".save-reward", function () {
        const index = $(this).data("index");
        const reward = $(this).siblings(".reward-name").val().trim();

        if (reward === "") {
            alert("Veuillez remplir le champ.");
            return;
        }

        // Mettre à jour les données
        console.log("Les données envoyées :", rewards[index].id);
        updateReward(rewards[index].id, reward);
    });

    // Écouteur pour supprimer un lien
    $(document).off("click", ".delete-reward").on("click", ".delete-reward", function () {
        const index = $(this).data("index");

        fetch("http://127.0.0.1:5000/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                id: rewards[index].id,
                ids: rewards[index].reward
            })
        });

        deleteReward(rewards[index].reward);
        rewards.splice(index, 1); // Supprimer l'élément correspondant à l'index
        renderRewards(); // Recharger les liens
    });
}

function updateLink(id, name, link){
    fetch("http://127.0.0.1:5000/link/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            id: id,
            name: name,
            link: link
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Erreur de création de lien.");
    }).then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });
}

function updateReward(id, reward){
    fetch("http://127.0.0.1:5000/reward/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            id: id,
            reward: reward,
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Erreur de création de récompense.");
    }).then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });
}

function deleteLink(id){
    fetch("http://127.0.0.1:5000/link/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            id: id
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Erreur de suppression de lien.");
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

function deleteReward(reward){

    fetch("http://127.0.0.1:5000/reward/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            reward: reward
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Erreur de suppression de récompense.");
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

function enableSpin() {
    canSpin = true;
    $("#spinButton").removeClass("disabled");
    $("#unlock-wheel").addClass("hidden");
}

function setupLinks(){
    getLinks().then(data => {
        data.links.forEach(link => {
            console.log(getCookie('links'));
            if((getCookie('links') || '[]').includes([link.id])){
                $(".popup-content").append(`<a id="link-${link.id}" href="${link.link}" class="disabled google-review-link">${link.name}</a>`);
            } else {
                $(".popup-content").append(`<a id="link-${link.id}" href="${link.link}" class="google-review-link">${link.name}</a>`);
            }
        });
        $(".google-review-link").off("click", ".google-review-link").on("click", function () {
            const id = $(this).attr("id").split("-")[1];
            enableSpin();
            let links = JSON.parse(getCookie('links') || '[]');
            validateReview(id)
            if(!links.includes(id)) {
                links.push([parseInt(id)]);
                setCookie('games', parseInt(getCookie('games')) + 1, 7);
            } else {
                clickLink(id);
            }
            $("#nb-games").text("Nombre de parties jouables : " + (parseInt(getCookie('games'))));
            setCookie('links', JSON.stringify(links), 7);
        });
        links.concat(data.links);
        renderLinks();
    });
}

function setupRewards(){
    getRewards().then(data => {
        rewards.concat(data.rewards);
        renderRewards();
    });
}

function getLinks(){
    return fetch("http://127.0.0.1:5000/links")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data;
    })
    .catch(error => {
        console.error(error);
    });
}

function addReward(reward){
    fetch("http://127.0.0.1:5000/customer/reward/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            reward: reward,
            phone: getCookie('phone')
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Erreur lors de l'ajout de la récompense.");
        }
    }
    ).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

function getRewards(){
    return fetch("http://127.0.0.1:5000/rewards")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data;
    })
    .catch(error => {
        console.error(error);
    });
}

function validateReview(link_id) {
    fetch("http://127.0.0.1:5000/review/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            user: getCookie('phone'),
            link_id: link_id
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Erreur de validation.");
        }
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
    canSpin = true;
}



function spin() {
    if(!canSpin)
        return;
    const reel1 = document.getElementById('reel1');
    const reel2 = document.getElementById('reel2');
    const reel3 = document.getElementById('reel3');
    const result = document.getElementById('result');
    setCookie('games', parseInt(getCookie('games')) - 1, 7);
    $("#nb-games").text("Nombre de parties jouables : " + getCookie('games'));

    fetch("http://127.0.0.1:5000/rewards")
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Erreur lors du spin.");
        }
    }).then(data => {
        data.rewards.forEach(reward => {
            possible_rewards.push(reward.reward);
        });

        // Symboles possibles
        const symbols = ["🍒", "🍋", "🍊", "⭐", "🍉", "🔔"];

        let finalSymbols = [];
        for (let i = 0; i < possible_rewards.length; i++) {
            finalSymbols.push(symbols[i]);
        }

        let winningReward = finalSymbols[Math.floor(Math.random() * finalSymbols.length)];

        // Poids des symboles
        const weights = Array(symbols.length).fill(0);
        weights[symbols.indexOf(winningReward)] = 1; // Le symbole gagnant a un poids de 1

        // find id of winning reward
        let winningRewardId = 0;
        data.rewards.forEach(reward => {
            if(reward.reward === possible_rewards[symbols.indexOf(winningReward)]){
                winningRewardId = reward.id;
            }
        });
        
        // Fonction pour choisir un symbole en fonction des probabilités
        function getRandomSymbol() {
            const totalWeight = weights.reduce((acc, weight) => acc + weight, 0); // Somme des poids
            const random = Math.random() * totalWeight; // Nombre aléatoire entre 0 et totalWeight
            let cumulativeWeight = 0;
        
            for (let i = 0; i < symbols.length; i++) {
                cumulativeWeight += weights[i];
                if (random < cumulativeWeight) {
                    return symbols[i]; // Retourne le symbole correspondant
                }
            }
        }
        

        // Fonction pour simuler le spin avec animation
        const spinReel = (reel, delay) => {
            reel.classList.add('spin'); // Ajoute l'animation
            setTimeout(() => {
                reel.classList.remove('spin'); // Arrête l'animation après délai
                reel.textContent = getRandomSymbol(); // Affiche un symbole aléatoire
            }, delay);
        };

        // Lancer chaque rouleau avec un délai différent
        // Pourquoi il n'y a plus de mammouths ?
        // Parce qu'il n'a plus de papoutes !
        spinReel(reel1, 700);
        spinReel(reel2, 900);
        spinReel(reel3, 1100);

        // Affiche le résultat après tous les spins
        setTimeout(() => {
            const r1 = reel1.textContent;
            const r2 = reel2.textContent;
            const r3 = reel3.textContent;

            if (r1 === r2 && r2 === r3) {
                result.innerHTML = "🎉 JACKPOT! Vous avez gagné :<br>" + possible_rewards[symbols.indexOf(winningReward)] + " ! 🎉";
                addReward(winningRewardId);
                let pastRewards = JSON.parse(getCookie('rewards') || '[]');
                pastRewards.push(possible_rewards[symbols.indexOf(winningReward)]);
                setCookie('rewards', JSON.stringify(pastRewards), 7);
                displayRewards(JSON.parse(getCookie('rewards')));
            } else {
                result.textContent = "😢 Essayez encore!";
            }
        }, 1200); // Assurez-vous que ce délai est supérieur au délai maximal des rouleaux
    }).catch(error => {
        console.error(error);
    });
    canSpin = getCookie('games') > 0;
}

function clickLink(link){
    fetch("http://127.0.0.1:5000/click", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            link: link,
            phone: getCookie('phone')
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Erreur lors du clic.");
        }
    }
    ).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000); // Convertir jours en millisecondes
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(value); // Assurez-vous d'encoder/décoder les cookies
        }
    }
    return null;
}

function login(phone, password){
    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            phone: phone,
            password: password,
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            $("#login-message").text("Erreur")
            throw new Error("Erreur de connexion.");
        }
    }).then(data => {
        if(!data.success) {
            $("#login-message").text("Mauvais mot de passe ou téléphone")
            throw new Error("Erreur de connexion.");
        }
        admin = data.data.role === "admin";
        if(admin)
            prefix = "admin-";
        setCookie('loggedInUser', data.data.role, 7);
        setCookie('phone', data.data.phone, 7);
        setCookie('visits', data.data.visits, 7);
        setCookie('games', data.data.games, 7);
        canSpin = data.canSpin;
        $('#login-section').addClass("hidden");
        $("header").removeClass("hidden");
        $("#" + prefix + "game-content").removeClass("hidden");
        $(".active").removeClass("active");
        $("#game").addClass("active");
        $("#visit-count").text(data.data.visits);
        $("#nb-games").text("Nombre de parties jouables : " + data.data.games);
        displayRewards(data.data.rewards);
        // refresh the page
        // save rewards in cookies
        setCookie('rewards',  JSON.stringify(data.data.rewards), 7);
        getLinksSaw(data.data.phone);
        setupLinks();
        if(admin) {
            setupRewards();
            getLinks().then(data => {
                links = data.links;
                renderLinks();
            }    
        );}
    }).catch(error => {
        console.error(error);
    });
}

function getLinksSaw(phone){
    fetch("http://127.0.0.1:5000/customer/links/" + phone).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Erreur de récupération des liens.");
        }
    }).then(data => {
        setCookie('links', JSON.stringify(data.links), 7);
    }).catch(error => {
        console.error(error);
    }
    );
}

function register(password, phone, birthdate, gender){
    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            phone: phone,
            password: password,
            birthdate, 
            gender: gender
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            $("#register-message").text("Erreur")
            throw new Error("Erreur d'inscription.");
        }
    }).then(data => {
        location.reload();
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
}

function addVisit(phone) {
    fetch("http://127.0.0.1:5000/visit/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
            phone: phone
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            $("#visit-message").text("Erreur lors de l'ajout de la visite.");
            throw new Error("Erreur dans la réponse du serveur.");
        }
    }).then(data => {
        if (!data.success) {
            $("#visit-message").text("Impossible d'ajouter la visite.");
            throw new Error("Erreur dans les données reçues.");
        }
        $("#visit-message").text("Visite ajoutée avec succès !");
        // reload the page
        location.reload();
    }).catch(error => {
        console.error("Erreur :", error);
    });
}

