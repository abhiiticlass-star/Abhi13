async function getSignal(){

const pair =
document.getElementById("pair").value;

const result =
document.getElementById("result");

result.innerHTML="Loading...";

try{

const res = await fetch(
"https://abhi13.onrender.com/get-signal/" + pair + "?tf=1"
);

const data = await res.json();

result.innerHTML = `
<h3>${data.signal}</h3>
<p>Score: ${data.score}</p>
<p>Trend: ${data.trend}</p>
<p>Support: ${data.support}</p>
<p>Resistance: ${data.resistance}</p>
`;

}catch(err){

result.innerHTML =
"API Error";

}

}
