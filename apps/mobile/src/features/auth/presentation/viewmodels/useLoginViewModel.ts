import { useMemo, useState } from "react";
import { LoginUseCase } from "../../domain/usecases/LoginUseCase";
import { AuthRepositoryMock } from "../../data/repositories/AuthRepositoryMock";
// para backend: reemplaza por el repo Http

const makeUseCase = () => new LoginUseCase(new AuthRepositoryMock());

export function useLoginViewModel() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const useCase = useMemo(makeUseCase, []);

  const submit = async () => {
    setLoading(true); setError(null);
    try {
      const user = await useCase.execute({ email, password });
      return { ok: true as const, user };
    } catch (e: any) {
      setError(e?.message ?? "Error desconocido");
      return { ok: false as const };
    } finally {
      setLoading(false);
    }
  };

  return { email, setEmail, password, setPassword, loading, error, submit };
}
