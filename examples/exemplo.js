// exemplo.js — função simples em JavaScript, incorporada na documentação
// via pymdownx.snippets (não existe handler de mkdocstrings para JS puro).

// Calcula a média aritmética de uma lista de números.
function calcularMedia(valores) {
  if (valores.length === 0) {
    throw new Error("A lista não pode estar vazia.");
  }
  return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
}

module.exports = { calcularMedia };
