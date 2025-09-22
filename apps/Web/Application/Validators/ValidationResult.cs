namespace Application.Validators
{
    /// <summary>
    /// Resultado de una validación con lista de errores.
    /// Facilita el manejo centralizado de errores de validación.
    /// </summary>
    public class ValidationResult
    {
        private readonly List<string> _errors;

        public ValidationResult()
        {
            _errors = new List<string>();
        }

        /// <summary>
        /// Indica si la validación fue exitosa (sin errores).
        /// </summary>
        public bool IsValid => !_errors.Any();

        /// <summary>
        /// Lista de errores encontrados durante la validación.
        /// </summary>
        public IReadOnlyList<string> Errors => _errors.AsReadOnly();

        /// <summary>
        /// Agrega un error a la lista de errores.
        /// </summary>
        public void AddError(string error)
        {
            if (!string.IsNullOrWhiteSpace(error))
            {
                _errors.Add(error);
            }
        }

        /// <summary>
        /// Agrega múltiples errores a la lista.
        /// </summary>
        public void AddErrors(IEnumerable<string> errors)
        {
            foreach (var error in errors.Where(e => !string.IsNullOrWhiteSpace(e)))
            {
                _errors.Add(error);
            }
        }

        /// <summary>
        /// Obtiene todos los errores concatenados en un solo string.
        /// </summary>
        public string GetErrorsAsString(string separator = "; ")
        {
            return string.Join(separator, _errors);
        }

        /// <summary>
        /// Limpia todos los errores.
        /// </summary>
        public void Clear()
        {
            _errors.Clear();
        }
    }
}