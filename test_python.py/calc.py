print("=== Simple Calculator ===")

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Choose operation:")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")

choice = input("Enter choice (1/2/3/4): ")

if choice == "1":
    result = num1 + num2
    print("Answer: " + str(result))
elif choice == "2":
    result = num1 - num2
    print("Answer: " + str(result))
elif choice == "3":
    result = num1 * num2
    print("Answer: " + str(result))
elif choice == "4":
    if num2 == 0:
        print("Error! Cannot divide by zero!")
    else:
        result = num1 / num2
        print("Answer: " + str(result))
else:
    print("Invalid choice!")

print("Thank you for using the calculator!")34