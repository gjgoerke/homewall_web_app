document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('boulderTable');
    const searchInput = document.getElementById('searchInput');
    const gradeMin = document.getElementById('gradeMin');
    const gradeMax = document.getElementById('gradeMax');
    const dateFilter = document.getElementById('dateFilter');

    // Sorting
    let currentSort = { column: null, direction: 'asc' };

    document.querySelectorAll('.sortable').forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.sort;
            const direction = currentSort.column === column && currentSort.direction === 'asc' ? 'desc' : 'asc';
            
            // Update sort state
            currentSort = { column, direction };
            
            // Sort the table
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.querySelector(`td[data-${column}]`).dataset[column];
                const bValue = b.querySelector(`td[data-${column}]`).dataset[column];
                
                if (column === 'grade') {
                    // Both are projects
                    if(aValue === 'None' && bValue === 'None') return 0;
                    // A is project (should be higher)
                    if(aValue === 'None') return direction === 'asc' ? -1 : 1;
                    // B is project (should be higher)
                    if(bValue === 'None') return direction === 'asc' ? 1 : -1;
                    
                    // Normal grade comparison
                    const result = direction === 'asc' ? 
                        parseInt(aValue) - parseInt(bValue) : 
                        parseInt(bValue) - parseInt(aValue);
                        
                    return result;
                }
                
                return direction === 'asc' ? 
                    aValue.localeCompare(bValue) : 
                    bValue.localeCompare(aValue);
            });

            // Clear and append sorted rows
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = '';
            sortedRows.forEach(row => tbody.appendChild(row));

            // Update sort indicators
            document.querySelectorAll('.sortable i').forEach(icon => {
                icon.className = 'bi bi-arrow-down-up';
            });
            th.querySelector('i').className = `bi bi-arrow-${direction === 'asc' ? 'up' : 'down'}`;
        });
    });

    // Filtering
    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const minGrade = parseInt(gradeMin.value) || 0;
        const maxGrade = parseInt(gradeMax.value) || 999;
        const filterDate = dateFilter.value;

        table.querySelectorAll('tbody tr').forEach(row => {
            const name = row.querySelector('td[data-name]').dataset.name.toLowerCase();
            const gradeData = row.querySelector('td[data-grade]').dataset.grade;
            const date = row.querySelector('td[data-date]').dataset.date;

            // Handle projects (null grades) differently
            const grade = gradeData ? parseInt(gradeData) : null;
            
            const matchesSearch = name.includes(searchTerm);
            const matchesGrade = grade === null || (grade >= minGrade && grade <= maxGrade);
            const matchesDate = !filterDate || date === filterDate;

            row.style.display = matchesSearch && matchesGrade && matchesDate ? '' : 'none';
        });
    }

    // Add event listeners for filters
    searchInput.addEventListener('input', filterTable);
    gradeMin.addEventListener('change', filterTable);
    gradeMax.addEventListener('change', filterTable);
    dateFilter.addEventListener('change', filterTable);
});