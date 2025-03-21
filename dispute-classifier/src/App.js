import React, { useState } from "react";
import axios from "axios";

function App() {
  const [disputeReason, setDisputeReason] = useState("");
  const [transactionAmount, setTransactionAmount] = useState("");
  const [pastDisputes, setPastDisputes] = useState("");
  const [customerId, setCustomerId] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = {
      customer_id: customerId,
      dispute_reason: disputeReason,
      transaction_amount: transactionAmount,
      past_disputes: pastDisputes,
    };

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/classify`, data);
      setResult(response.data);
    } catch (error) {
      console.error("There was an error classifying the dispute:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Dispute Classification and Routing</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Customer ID:</label>
          <input
            type="text"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Dispute Reason:</label>
          <input
            type="text"
            value={disputeReason}
            onChange={(e) => setDisputeReason(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Transaction Amount:</label>
          <input
            type="number"
            value={transactionAmount}
            onChange={(e) => setTransactionAmount(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Number of Past Disputes:</label>
          <input
            type="number"
            value={pastDisputes}
            onChange={(e) => setPastDisputes(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Classifying..." : "Classify Dispute"}
        </button>
      </form>

      {result && (
        <div>
          <h2>Result:</h2>
          <p>Dispute Type: {result.dispute_type}</p>
          <p>Priority Level: {result.priority_level}</p>
          <p>High-Risk: {result.high_risk ? "Yes" : "No"}</p>
          <p>Recommended Team: {result.recommended_team}</p>
        </div>
      )}
    </div>
  );
}

export default App;
