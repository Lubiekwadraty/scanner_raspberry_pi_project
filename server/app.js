const express = require('express')
const cors = require('cors')
const mariadb = require('mariadb');
const app = express()
const port = 3000

app.use(cors())


app.get("/api/personAction", async (req, res) => {
    let conn;
    try {
        conn = await pool.getConnection(); // Get a connection from the pool
        console.log(req.query);
        let worker_id = req.query.worker_id;
        let code = req.query.code;
        let check = await conn.query(`SELECT code FROM event_types`);

        const codes = check.map((e) => e.code)
        if(!codes.includes(code)){
            res.send(400);
        }
        else{
            let row = await conn.query(`SELECT id FROM event_types WHERE code=?`, [code]);
            await conn.query(`INSERT INTO event_log(worker_id, type_id) VALUES (?, ?)`, [worker_id, row[0].id]);
            res.sendStatus(200);
        }
        
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

app.get("/api/personData", async (req, res) => {
        // const rows = await executeDatabaseOperations();
    let conn;
    try {
        conn = await pool.getConnection(); // Get a connection from the pool
        console.log(Object.values(req.query)[0]);
        let code = Object.values(req.query)[0];
        // if(isNaN(code)){
        //     res.status(400).send("invalid code");
        // }
        // else{
            // --- SELECT Query ---
            const rows = await conn.query(`SELECT workers.id, workers.first_name FROM workers LEFT JOIN barcodes ON workers.id = barcodes.employee_id LEFT JOIN rfids ON workers.id = rfids.employee_id WHERE barcodes.code=? OR rfids.code=?;;`, [code, code]);
            console.log("Selected Rows:", rows);
            // res.sendStatus(400);
            res.json(rows);
        // }
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
    host: `localhost`,
    user: 'root', 
    password: '', //you need to add password for your mariadDB database
    database: 'kPoint',
    connectionLimit: 10
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