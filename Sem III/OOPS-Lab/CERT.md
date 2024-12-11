# CERT Java Secure Coding Standards

## Expressions (EXP)

### EXP00-J: Do not ignore values returned by methods

Always use or handle return values from method calls to ensure proper program logic and prevent potential bugs.

**Example of Non-Compliant Code:**
```java
"Hello, World!".toUpperCase(); // Ignored return value
```

**Compliant Solution:**
```java
String result = "Hello, World!".toUpperCase(); // Use the returned value
System.out.println(result);
```

**Explanation:**
- Ignoring return values can lead to missed error handling or unintended behavior
- Methods often return important information that should be processed or at least acknowledged
- Always capture or use the return value when it provides meaningful information

### EXP01-J: Never dereference null pointers

Always check for null before accessing object methods or properties to prevent NullPointerException.

**Example of Non-Compliant Code:**
```java
String str = null;
System.out.println(str.length()); // NullPointerException
```

**Compliant Solution:**
```java
String str = null;
if (str != null) {
    System.out.println(str.length());
} else {
    System.out.println("String is null.");
}
```

**Explanation:**
- Null checks prevent unexpected runtime exceptions
- Provides a safe way to handle potentially uninitialized objects
- Improves code robustness and error handling

### EXP02-J: Use the two-argument Arrays.equals() method to compare array contents

Use `Arrays.equals()` for accurate array content comparison instead of reference comparison.

**Example of Non-Compliant Code:**
```java
int[] arr1 = {1, 2, 3};
int[] arr2 = {1, 2, 3};
System.out.println(arr1 == arr2); // Always false (compares references)
```

**Compliant Solution:**
```java
int[] arr1 = {1, 2, 3};
int[] arr2 = {1, 2, 3};
System.out.println(Arrays.equals(arr1, arr2)); // Correctly compares contents
```

**Explanation:**
- `==` compares object references, not array contents
- `Arrays.equals()` performs deep comparison of array elements
- Works for primitive and object arrays

## Numeric Operations (NUM)

### NUM00-J: Detect or prevent integer overflow

Check for potential integer overflow before performing arithmetic operations that might exceed type limits.

**Example of Non-Compliant Code:**
```java
int max = Integer.MAX_VALUE;
int result = max + 1; // Overflow occurs
```

**Compliant Solution:**
```java
int max = Integer.MAX_VALUE;
if (max == Integer.MAX_VALUE) {
    System.out.println("Overflow would occur!");
} else {
    int result = max + 1;
}
```

**Explanation:**
- Integer overflow can lead to unexpected and potentially dangerous results
- Use explicit checks or consider using `Math.addExact()` for safe additions
- For large number calculations, consider using `long` or `BigInteger`

### NUM01-J: Do not perform bitwise and arithmetic operations on the same data

Separate bitwise and arithmetic operations to maintain code clarity and prevent unexpected results.

**Example of Non-Compliant Code:**
```java
int num = 5;
int result = (num << 1) + num; // Mixed bitwise and arithmetic
```

**Compliant Solution:**
```java
int num = 5;
int result = num * 3; // Avoid combining bitwise and arithmetic
```

**Explanation:**
- Mixing bitwise and arithmetic operations can lead to confusing and error-prone code
- Separate these operations for better readability and maintainability
- Use clear, explicit calculations

### NUM02-J: Prevent divide-by-zero errors

Always check for zero before performing division or modulo operations.

**Example of Non-Compliant Code:**
```java
int num = 10;
int result = num / 0; // ArithmeticException
```

**Compliant Solution:**
```java
int num = 10, divisor = 0;
if (divisor != 0) {
    int result = num / divisor;
} else {
    System.out.println("Division by zero is not allowed.");
}
```

**Explanation:**
- Division by zero throws an ArithmeticException
- Always validate divisors before performing division
- Provide alternative handling or error messaging

### NUM03-J: Use appropriate integer types

Choose integer types that can fully represent the range of your data to prevent unexpected overflow.

**Example of Non-Compliant Code:**
```java
short value = 32767; // Max value for short
value += 1;          // Overflow to negative
```

**Compliant Solution:**
```java
int value = 32767; // Use int for larger range
value += 1;
```

**Explanation:**
- Choose integer types based on expected value ranges
- `int` provides a larger range than `short`
- Prevent unintended overflow by selecting appropriate types

### NUM04-J: Avoid floating-point imprecision

Use `BigDecimal` for precise numerical computations requiring exact representation.

**Example of Non-Compliant Code:**
```java
double value = 0.1 + 0.2; // Imprecise due to floating-point representation
System.out.println(value == 0.3); // False
```

**Compliant Solution:**
```java
BigDecimal value = BigDecimal.valueOf(0.1).add(BigDecimal.valueOf(0.2));
System.out.println(value.equals(BigDecimal.valueOf(0.3))); // True
```

**Explanation:**
- Floating-point arithmetic can introduce small imprecisions
- `BigDecimal` provides exact decimal representation
- Use for financial calculations or when precision is critical

### NUM05-J: Avoid denormalized numbers

Prevent calculations that might produce denormalized (extremely small) floating-point numbers.

**Example of Non-Compliant Code:**
```java
double value = 1e-308 / 1e10; // May produce denormalized numbers
```

**Compliant Solution:**
```java
double value = Math.max(1e-308, 1e-10); // Avoid results prone to denormalization
```

**Explanation:**
- Denormalized numbers can cause performance and precision issues
- Use techniques to avoid extremely small floating-point values
- Understand the limitations of floating-point arithmetic

## Methods (MET)

### MET00-J: Validate method arguments

Always validate method arguments to ensure data integrity and prevent invalid state.

**Example of Non-Compliant Code:**
```java
public void setAge(int age) {
    this.age = age; // No validation
}
```

**Compliant Solution:**
```java
public void setAge(int age) {
    if (age < 0 || age > 150) {
        throw new IllegalArgumentException("Invalid age: " + age);
    }
    this.age = age;
}
```

**Explanation:**
- Validate input parameters to maintain object invariants
- Throw appropriate exceptions for invalid inputs
- Prevent setting objects into inconsistent states

### MET03-J: Secure method accessibility

Declare security-related methods as private to prevent external access.

**Example of Non-Compliant Code:**
```java
public boolean isAuthenticated(User user) {
    // Security check logic
    return true;
}
```

**Compliant Solution:**
```java
private boolean isAuthenticated(User user) {
    // Security check logic
    return true;
}
```

**Explanation:**
- Security-sensitive methods should not be publicly accessible
- Use private modifier to restrict method visibility
- Prevent potential security vulnerabilities

### MET04-J: Maintain method accessibility during inheritance

Ensure overridden methods do not increase accessibility.

**Example of Non-Compliant Code:**
```java
class Parent {
    protected void display() {}
}
class Child extends Parent {
    public void display() {} // Increases accessibility
}
```

**Compliant Solution:**
```java
class Parent {
    protected void display() {}
}
class Child extends Parent {
    @Override
    protected void display() {} // Maintains accessibility
}
```

**Explanation:**
- Override methods must maintain or reduce (not increase) the accessibility of the parent method
- Use `@Override` annotation to ensure correct method signature
- Prevent unintended exposure of methods during inheritance
