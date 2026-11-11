/**
 * Calcula a média de uma lista de valores.
 *
 * @param valores - Lista de valores numéricos.
 * @returns Média aritmética dos valores.
 * @throws {Error} Se a lista estiver vazia.
 */
export function calcularMedia(valores: number[]): number {
  if (valores.length === 0) {
    throw new Error("A lista não pode estar vazia.");
  }

  return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
}
