const express = require('express')
const cors = require('cors')
const mariadb = require('mariadb');
const app = express()
const port = 3000

app.use(cors())



app.get("/api/personData", async (req, res) => {
        // const rows = await executeDatabaseOperations();
    let conn;
    try {
        conn = await pool.getConnection(); // Get a connection from the pool

        // --- SELECT Query ---
        const rows = await conn.query(`SELECT workers.id, workers.name, barcodes.code FROM workers JOIN barcodes ON workers.id = barcodes.employee_id WHERE workers.id=1;`, ["active"]);
        console.log("Selected Rows:", rows);
        // res.sendStatus(400);
        res.json(rows);
        console.log(req.query)
    } catch (err) {
        console.error("Database operation error:", err);
        throw err; // Re-throw to handle higher up
    } finally {
        if (conn) {
            conn.release(); // Release connection back to the pool
            console.log("Connection released to pool.");
        }
    }
    })

const pool = mariadb.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'kpoint',
    connectionLimit: 5
});

async function executeDatabaseOperations() {
    let conn;
    try {
        conn = await pool.getConnection(); // Get a connection from the pool

        // --- SELECT Query ---
        const rows = await conn.query(`SELECT * FROM workers WHERE id=123 `, ["active"]);
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