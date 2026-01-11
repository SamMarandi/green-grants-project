document.addEventListener("DOMContentLoaded", function () {
    const screen1 = document.getElementById('screen1');
    const screen2 = document.getElementById('screen2');
    const subsidyForm = document.getElementById('subsidyForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const backBtn = document.getElementById('backBtn');
    const modal = document.getElementById('modal');
    const closeModal = document.querySelector('.close');

    if (screen1 && screen2 && resultsContainer && backBtn && modal && closeModal) {

        function displayResults(subsidies) {
            resultsContainer.innerHTML = '';

            if (!subsidies || subsidies.length === 0) {
                resultsContainer.innerHTML = `
                    <div class="no-results">
                        <h2>No Matching Subsidies Found</h2>
                        <p>Try selecting different areas of interest or check back later for new programs.</p>
                    </div>
                `;
                return;
            }

            subsidies.forEach(subsidy => {
                const card = document.createElement('div');
                card.className = 'subsidy-card';
                card.innerHTML = `
                    <div class="subsidy-header">
                        <h2 class="subsidy-title">${subsidy.title}</h2>
                        <span class="subsidy-level">${subsidy.level}</span>
                    </div>
                    <div class="subsidy-benefit">${subsidy.benefit}</div>
                    <p class="subsidy-description">${subsidy.description}</p>
                    <button class="btn-see-more" data-id="${subsidy.id}">See More</button>
                `;

                const seeMoreBtn = card.querySelector('.btn-see-more');
                seeMoreBtn.addEventListener('click', () => {
                    showModal(subsidy);
                });

                resultsContainer.appendChild(card);
            });
        }

        function showModal(subsidy) {
            document.getElementById('modalTitle').textContent = subsidy.title;
            document.getElementById('modalDescription').textContent = subsidy.description;
            document.getElementById('modalEligibility').textContent = subsidy.eligibility;
            modal.classList.add('active');
        }

        backBtn.addEventListener('click', () => {
            screen2.classList.remove('active');
            screen1.classList.add('active');
            window.scrollTo(0, 0);
        });

        closeModal.addEventListener('click', () => {
            modal.classList.remove('active');
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    }

    const openBtn = document.getElementById("openFilter");
    const filterModal = document.getElementById("filterModal");
    const closeBtn = document.getElementById("closeFilter");

    if (openBtn && filterModal && closeBtn) {

        openBtn.addEventListener("click", () => {
            filterModal.classList.add("show");
        });

        closeBtn.addEventListener("click", () => {
            filterModal.classList.remove("show");
        });

        filterModal.addEventListener("click", (e) => {
            if (e.target === filterModal) {
                filterModal.classList.remove("show");
            }
        });
    }
});
