import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class StudentDatabaseApp {
    private JFrame frame;
    private JTable table;
    private JTextField idField, nameField, ageField;
    private DefaultTableModel tableModel;

    // Database connection details
    private final String DB_URL = "jdbc:sqlite:db.db";

    public StudentDatabaseApp() {
        frame = new JFrame("Student Database");

        // Setting up the table columns
        String[] columnNames = {"ID", "Name", "Age"};
        tableModel = new DefaultTableModel(columnNames, 0);
        table = new JTable(tableModel);
        JScrollPane tablePane = new JScrollPane(table);

        // Creating the input fields
        JPanel inputPanel = new JPanel();
        inputPanel.setLayout(new GridLayout(2, 3, 5, 5));
        inputPanel.add(new JLabel("ID:"));
        inputPanel.add(new JLabel("Name:"));
        inputPanel.add(new JLabel("Age:"));

        idField = new JTextField(5);
        nameField = new JTextField(20);
        ageField = new JTextField(10);
        inputPanel.add(idField);
        inputPanel.add(nameField);
        inputPanel.add(ageField);

        // Add Data button
        JButton addButton = new JButton("Add Data");
        addButton.addActionListener(e -> addData());

        // Refresh button to reload data from the database
        JButton refreshButton = new JButton("Refresh Data");
        refreshButton.addActionListener(e -> populateTable());

        // Adding components to the frame
        frame.setLayout(new BorderLayout());
        frame.add(tablePane, BorderLayout.CENTER);
        frame.add(inputPanel, BorderLayout.NORTH);

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(addButton);
        buttonPanel.add(refreshButton);
        frame.add(buttonPanel, BorderLayout.SOUTH);

        // Frame settings
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        // Initial population of the table with data from the database
        populateTable();
    }

    // Method to establish a connection with the SQLite database
    private Connection connect() {
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(DB_URL);
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(frame, "Connection to database failed: " + e.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        }
        return conn;
    }

    // Method to fetch data from the 'students' table and populate the table
    private void populateTable() {
        Connection conn = connect();
        if (conn == null) return;

        // Clear existing data in the table
        tableModel.setRowCount(0);

        String query = "SELECT id, name, age FROM students";
        try (Statement stmt = conn.createStatement(); ResultSet rs = stmt.executeQuery(query)) {
            while (rs.next()) {
                String id = rs.getString("id");
                String name = rs.getString("name");
                String age = rs.getString("age");
                tableModel.addRow(new Object[]{id, name, age});
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(frame, "Error fetching data: " + e.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        } finally {
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    // Method to add new data into the 'students' table
    private void addData() {
        String id = idField.getText();
        String name = nameField.getText();
        String age = ageField.getText();

        // Ensure all fields are filled
        if (id.isEmpty() || name.isEmpty() || age.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Please fill all fields", "Input Error", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Connection conn = connect();
        if (conn == null) return;

        String query = "INSERT INTO students (id, name, age) VALUES (?, ?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(query)) {
            pstmt.setString(1, id);
            pstmt.setString(2, name);
            pstmt.setString(3, age);
            pstmt.executeUpdate();

            // Clear the input fields after insertion
            idField.setText("");
            nameField.setText("");
            ageField.setText("");

            // Show success message
            JOptionPane.showMessageDialog(frame, "Data inserted successfully", "Success", JOptionPane.INFORMATION_MESSAGE);

            // Repopulate the table to reflect the new data
            populateTable();
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(frame, "Error inserting data: " + e.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        } finally {
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(StudentDatabaseApp::new);
    }
}
