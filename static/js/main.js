document.addEventListener("DOMContentLoaded", () => {

  // Helper to show simple toast notifications (native)
  function toast(text) {
    const el = document.createElement('div');
    el.textContent = text;
    el.style.position = 'fixed';
    el.style.right = '18px';
    el.style.bottom = '18px';
    el.style.background = '#222';
    el.style.color = '#fff';
    el.style.padding = '10px 14px';
    el.style.borderRadius = '8px';
    el.style.boxShadow = '0 6px 18px rgba(0,0,0,0.6)';
    document.body.appendChild(el);
    setTimeout(()=> el.remove(), 2500);
  }

  // Delete expense via AJAX
  document.querySelectorAll('.deleteExpenseBtn').forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      const id = btn.getAttribute('data-id');
      if (!confirm('Delete this expense?')) return;
      try {
        const res = await fetch(`/api/expenses/${id}`, { method:'DELETE' });
        const j = await res.json();
        if (j.ok) {
          const row = document.getElementById(`exp-${id}`);
          if (row) row.remove();
          toast('Expense deleted');
          // Refresh chart by fetching fresh data (simple approach: reload)
          location.reload();
        } else {
          toast('Failed to delete');
        }
      } catch(err){
        toast('Network error');
      }
    });
  });

  // Edit expense: pop modal with data
  const editModalEl = document.getElementById('editExpenseModal');
  const editModal = new bootstrap.Modal(editModalEl);
  document.querySelectorAll('.editExpenseBtn').forEach(btn=>{
    btn.addEventListener('click', (e) => {
      const expense = JSON.parse(btn.getAttribute('data-expense') || "{}");
      document.getElementById('editExpenseId').value = expense.id;
      document.getElementById('editCategory').value = expense.category;
      document.getElementById('editAmount').value = expense.amount;
      document.getElementById('editNote').value = expense.note || '';
      document.getElementById('editDate').value = expense.date || '';
      editModal.show();
    });
  });

  // Handle edit submission
  document.getElementById('editExpenseForm').addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const id = document.getElementById('editExpenseId').value;
    const payload = {
      category: document.getElementById('editCategory').value,
      amount: document.getElementById('editAmount').value,
      note: document.getElementById('editNote').value,
      date: document.getElementById('editDate').value
    };
    try {
      const res = await fetch(`/api/expenses/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const j = await res.json();
      if (j.ok) {
        toast('Expense updated');
        editModal.hide();
        // update row UI quickly (or reload)
        location.reload();
      } else {
        toast(j.error || 'Update failed');
      }
    } catch(err) {
      toast('Network error');
    }
  });

  // Delete budget
  const delBudgetBtn = document.getElementById('deleteBudgetBtn');
  if (delBudgetBtn) {
    delBudgetBtn.addEventListener('click', async (e)=>{
      const id = delBudgetBtn.getAttribute('data-budget-id');
      if (!confirm('Delete current budget?')) return;
      try {
        const res = await fetch(`/api/budget/${id}`, { method: 'DELETE' });
        const j = await res.json();
        if (j.ok) {
          toast('Budget deleted');
          location.reload();
        } else toast('Failed to delete budget');
      } catch(err){
        toast('Network error');
      }
    });
  }

  // Export CSV on reports page
  const exportBtn = document.getElementById('exportCsvBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', ()=>{
      // build CSV from table data
      const rows = Array.from(document.querySelectorAll('table tbody tr'));
      const csv = [['Category','Amount','Note','Date']];
      rows.forEach(r=>{
        const cols = Array.from(r.querySelectorAll('td')).map(td => td.innerText.trim().replace(/\$/g,''));
        csv.push(cols);
      });
      const csvText = csv.map(r => r.map(c => `"${c.replace(/"/g,'""')}"`).join(',')).join('\n');
      const blob = new Blob([csvText], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'expenses.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

});
