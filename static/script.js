function fetchCommits() {
    fetch('/api/commits')  // ✅ Fetch the latest commit from Flask API
        .then(response => response.json())
        .then(commit_list => {
            let commitList = document.getElementById("commit-list");
            commitList.innerHTML = ""; // Clear previous commits

            if (commit_list.error) {
                commitList.innerHTML = `<li style="color: red;">Error: ${commit_list.error}</li>`;
                return;
            }

            // ✅ Create Table for Commit Details
            let tableHTML = `
                <table class="commit-list-container">
                    <tr>
                        <th>Commit ID</th>
                        <th>Author</th>
                        <th>Message</th>
                        <th>Date</th>
                    </tr>
                    <tr>
                        <td><strong>${commit_list.sha.substring(0, 7)}...</strong></td>  <!-- Shortened Commit ID -->
                        <td><strong>${commit_list.author}</strong></td>
                        <td>${commit_list.message}</td>
                        <td>${commit_list.date}</td>
                    </tr>
                </table>
            `;

            commitList.innerHTML = tableHTML; // ✅ Append table to UI
        })
        .catch(error => {
            console.error("Error fetching commit:", error);
            document.getElementById("commit-list").innerHTML = `<li style="color: red;">Failed to load commit.</li>`;
        });
}
