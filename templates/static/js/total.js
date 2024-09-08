function calculateTotal(barbeiroId) {
    let total = 0;
    let checkboxes = document.querySelectorAll('input[name="servicos"]:checked');
    
    checkboxes.forEach(function(checkbox) {
        let valor = parseFloat(checkbox.getAttribute('data-valor'));
        total += valor;
    });

    // Atualiza o total na interface do usuário
    document.getElementById(`total-${barbeiroId}`).textContent = total.toFixed(2);
    // Atualiza o campo oculto com o valor total
    document.getElementById(`total-hidden-${barbeiroId}`).value = total.toFixed(2);
}
