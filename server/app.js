const express = require('express')
const cors = require('cors')
const mariadb = require('mariadb');
const app = express()
const port = 3000

app.use(cors())


app.get("/api/personData", async (req, res) => {
    const rows = await executeDatabaseOperations()
    res.json(rows);
})

const pool = mariadb.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'kPoint',
    connectionLimit: 5
});

async function executeDatabaseOperations(barcode) {
    let conn;
    try {
        conn = await pool.getConnection(); // Get a connection from the pool

        // --- SELECT Query ---
        const rows = await conn.query(`SELECT * FROM workers WHERE barcode_id ="${barcode}" `, ["active"]);
        console.log("Selected Rows:", rows);
        return rows;
    } catch (err) {
        console.error("Database operation error:", err);
        throw err; // Re-throw to handle higher up
    } finally {
        if (conn) {
            conn.release(); // Release connection back to the pool
            console.log("Connection released to pool.");
        }
    }
}


app.listen(port, () => {
    console.log(`listening on port ${port}`)
})