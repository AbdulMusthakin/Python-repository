def integrate(f, a, b, n):
  integral = f(a) + f(b)
  h = (b-a)/n
  for i in range(1, n):
    integral += 2*f(a + i*h)
  integral *= h * 0.5
  return integral
