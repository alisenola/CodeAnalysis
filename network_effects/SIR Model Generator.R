# Import libraries
library(deSolve)
library(FME)

# Declare the dynamic model function
# Returns the derivatives of S, I and R (in # of people, NOT NORMALIZED!)
sir <- function(time,state,parameters) {
  with(as.list(c(state,parameters)), {
    dR <- gamma*I
    dI <- beta*S - dR
    dS <- -(dI + dR)
    return(list(c(dS,dI,dR)))
  })
}

# Specify arbitrary ICs and parameters (for the whole population DO NOT NORMALIZE!)
init_unfitted <- c(S=100,I=2,R=0)
parameters_unfitted <- c(beta=0.1, gamma=0.14)
times <- seq(0, 38, by=1)

# Solve based on these arbitrary ICs (to make sure it works) 
out <- ode(y=init_unfitted, times=times, func=sir, parms=parameters_unfitted)
out <- as.data.frame(out)
head(out,10)

# Plot the solved data from arbitrary ICs
matplot(x = times, y = out, type = "l",
        xlab = "Time", ylab = "# of People", main = "SIR Model",
        lwd = 1, lty = 1, bty = "l", col = 2:4)
legend(2, 80, c("Susceptible", "Infected", "Recovered"), pch = 1, col = 2:4, bty = "n")



##########################################################################################
# Fit the parameters AND the initial conditions to real data
##########################################################################################

# Load the real data to fit to the model
setwd("C:\\Users\\lmeng\\Github\\CrimsonCodeAnalysis\\network_effects")
wow_activations <- read.csv(file="wow_activations.csv", head=TRUE)
wow_activations
plot(wow_activations)

# Initial guesses for the parameters
parameters_fitted <- c(S=26,beta=0.05,gamma=0.06)
init_fitted <- c(I=2,R=0)

# Cost function
cost <- function(p, S) {
  yy <- p[c("S")]
  pp <- p[c("beta", "gamma")]
  out <- ode(c(yy,init_fitted), times=times, func=sir, pp)
  modCost(out, wow_activations, weight = "none") # can also use "std" or "mean" weighting
}

# Fit the function (TODO: Look into why results vary wildly based on optimization method)
fit <- modFit(f = cost, p = parameters_fitted, lower=0, upper=7e9)
summary(fit)

# Generated un-fitted curves
out_unfitted <- ode(init_unfitted, times, sir, parameters_unfitted)
# Generate fitted curves
out_fitted <- ode(c(coef(fit)[1],init_fitted), times, sir, coef(fit)[2:3])
# Plot
plot(out_unfitted, out_fitted, obs=wow_activations, col=2:4)
par(xpd=TRUE)
legend(1,1,c("Un-fitted", "Fitted", "Observed"), pch = 1, col = 2:4, bty = "n")

##########################################################################################

# ##########################################################################################
# OLD - Fit the parameters ONLY
# ##########################################################################################

# parameters_oldfit <- c(beta=1,gamma=1)
# init_oldfit <- c(S=100,I=2,R=0)

# # Define cost function to calculate error
# cost <- function(parameters) {
#   # yy <- p[c("S","I","R")]
#   # pp <- p[c("beta", "gamma")]
#   out <- ode(y=init_oldfit, times=times, func=sir, parms=parameters)
#   modCost(out, wow_activations, weight = "none") # can also use "std" or "mean" weighting
# }

# # Fit the parameters by minimizing objective cost function
# fit <- modFit(f = cost, p = parameters_oldfit)
# summary(fit)


# # Generate un-fitted and fitted infection curves
# out1 <- ode(init, times, sir, parameters)
# out2 <- ode(init, times, sir, coef(fit))

# # Plot along with observed data
# plot(out1, out2, obs=wow_activations, col=2:4)
# par(xpd=TRUE)
# legend(2, 80, c("Un-fitted", "Fitted", "Observed"), pch = 1, col = 2:4, bty = "n")
# # ##########################################################################################

























